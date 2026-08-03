#!/usr/bin/env python3
"""
Production-Grade Data Fetcher & Project Merger

Fetches, filters, scores, and merges GitHub repository metrics and byte-weighted
language statistics with resilience (session pooling, retries, caching, and validation).
"""

import json
import os
import sys
import time
from typing import List, Dict, Any, Tuple
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# --- UPDATED CONFIGURATION ---
USERNAME = "BandiHemaVenkataSaiSriBhavya" # Your GitHub Username
USER_EMAIL = "bandihemavenkatasaisribhavya@gmail.com" # Your Contact Email
CACHE_FILE = "cache/github.json"
CACHE_EXPIRY_SECONDS = 3600  # 1 Hour
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()


def get_resilient_session() -> requests.Session:
    """Configures a requests session with connection pooling and backoff retries."""
    session = requests.Session()
    session.headers.update({
        "Accept": "application/vnd.github+json",
        "User-Agent": f"github-profile-banner-{USERNAME}", 
    })
    if GITHUB_TOKEN:
        session.headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def load_cached_data() -> Tuple[bool, List[Dict[str, Any]]]:
    """Loads GitHub API responses from local cache if younger than 1 hour."""
    if not os.path.exists(CACHE_FILE):
        return False, []
    
    try:
        mtime = os.path.getmtime(CACHE_FILE)
        if (time.time() - mtime) < CACHE_EXPIRY_SECONDS:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"[INFO] Loaded {len(data)} repositories from valid local cache.")
                return True, data
    except Exception as e:
        print(f"[WARN] Failed to read cache: {e}")
    
    return False, []


def save_cache_data(data: List[Dict[str, Any]]) -> None:
    """Saves raw API data to disk cache."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("[INFO] Successfully saved API response to local cache.")
    except Exception as e:
        print(f"[WARN] Could not write to cache file: {e}")


def fetch_all_repos(session: requests.Session) -> List[Dict[str, Any]]:
    """Paginates through GitHub API to retrieve all public user repositories."""
    is_cached, cached_repos = load_cached_data()
    if is_cached:
        return cached_repos

    print(f"[INFO] Fetching user repositories for {USERNAME} from GitHub API...")
    url = f"https://api.github.com/users/{USERNAME}/repos"
    page = 1
    repos: List[Dict[str, Any]] = []

    while True:
        try:
            resp = session.get(url, params={"per_page": 100, "page": page, "sort": "pushed"}, timeout=20)
            resp.raise_for_status()
            data = resp.json()

            if not data:
                break

            repos.extend(data)
            print(f"[INFO] Fetched page {page} ({len(data)} repos)")
            page += 1
        except Exception as e:
            print(f"[ERROR] GitHub API fetch error on page {page}: {e}")
            break

    # Filter out forks, archived repos, templates, and empty repos
    filtered_repos = [
        r for r in repos
        if not r.get("fork", False)
        and not r.get("archived", False)
        and not r.get("is_template", False)
        and r.get("size", 0) > 0
    ]

    print(f"[INFO] Retained {len(filtered_repos)} source repos out of {len(repos)} total.")
    save_cache_data(filtered_repos)
    return filtered_repos


def calculate_project_score(repo_data: Dict[str, Any]) -> float:
    """Calculates weighted project quality score for auto-ranking."""
    stars = repo_data.get("stargazers_count", 0)
    forks = repo_data.get("forks_count", 0)
    watchers = repo_data.get("watchers_count", 0)
    size_kb = repo_data.get("size", 0)

    # Scoring formula: Stars heavily weighted, size adds minor bonus
    return (stars * 5.0) + (forks * 3.0) + (watchers * 1.0) + (size_kb / 100.0)


def fetch_repo_languages(session: requests.Session, repo_name: str) -> Dict[str, int]:
    """Retrieves byte-level language metrics for a given repo."""
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/languages"
    try:
        resp = session.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"[WARN] Failed to fetch language bytes for {repo_name}: {e}")
    return {}


def process_and_merge() -> None:
    session = get_resilient_session()
    
    # 1. Load user curated list (projects.json must exist)
    curated_projects = []
    if os.path.exists("projects.json"):
        with open("projects.json", "r", encoding="utf-8") as f:
            try:
                curated_projects = json.load(f)
                print(f"[INFO] Loaded {len(curated_projects)} curated project definitions from projects.json")
            except Exception as e:
                print(f"[ERROR] Failed to read projects.json: {e}")
    else:
        print("[WARN] projects.json not found. Proceeding with auto-discovery only.")

    # 2. Fetch live repos
    live_repos = fetch_all_repos(session)
    live_repo_map = {r["name"].lower(): r for r in live_repos}

    merged_projects: List[Dict[str, Any]] = []

    if curated_projects:
        print("[INFO] Merging curated list with live data and fetching language stats...")
        for p in curated_projects:
            # Extract repo name safely from URL or name field
            raw_repo = p.get("repo", "")
            if "/" in raw_repo:
                 repo_name = raw_repo.split("/")[-1]
            else:
                 repo_name = raw_repo
                 
            matched_live = live_repo_map.get(repo_name.lower(), {})

            # Standardize fields
            p["repo"] = f"{USERNAME}/{repo_name}"
            p["stars"] = matched_live.get("stargazers_count", p.get("stars", 0))
            p["pushed_at"] = matched_live.get("pushed_at", None)
            
            if not p.get("description"):
                p["description"] = matched_live.get("description", "")

            # Get byte breakdown (language statistics)
            if repo_name:
                p["languages"] = fetch_repo_languages(session, repo_name)
            else:
                p.setdefault("languages", {})

            merged_projects.append(p)
    else:
        # Fallback to auto-discovering top scored repositories if projects.json is empty
        print("[INFO] No projects.json found. Auto-discovering top repositories based on quality score...")
        scored_repos = sorted(live_repos, key=calculate_project_score, reverse=True)[:6]
        
        for r in scored_repos:
            repo_name = r["name"]
            merged_projects.append({
                "name": repo_name,
                "repo": f"{USERNAME}/{repo_name}",
                "description": r.get("description", ""),
                "stars": r.get("stargazers_count", 0),
                "pushed_at": r.get("pushed_at"),
                "languages": fetch_repo_languages(session, repo_name)
            })

    # 3. Validation Pass
    print("[INFO] Validating output data...")
    if not merged_projects:
        print("[ERROR] Output project list is empty! Aborting merge.")
        sys.exit(1)

    for idx, proj in enumerate(merged_projects):
        if not proj.get("name"):
            proj["name"] = f"Project #{idx + 1}"
        proj.setdefault("stars", 0)
        proj.setdefault("description", "")

    # 4. Write merged output to merged.json
    print("[INFO] Writing merged.json...")
    try:
        with open("merged.json", "w", encoding="utf-8") as f:
            json.dump(merged_projects, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Successfully output {len(merged_projects)} merged project records.")
    except Exception as e:
        print(f"[ERROR] Failed to write merged.json: {e}")
        sys.exit(1)

if __name__ == "__main__":
    process_and_merge()