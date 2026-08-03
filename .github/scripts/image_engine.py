#!/usr/bin/env python3
import os
import random
import sys

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow (PIL) is not installed. Run: pip install Pillow", file=sys.stderr)
    exit(1)

def generate_dot_portrait_svg(image_path, target_cols=130, target_rows=160):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}", file=sys.stderr)
        return ""

    try:
        # Convert to RGB to keep your exact original photo colors
        img = Image.open(image_path).convert("RGB")
        # High resolution grid for extreme clarity
        img = img.resize((target_cols, target_rows), Image.Resampling.LANCZOS)
        pixels = img.load()
    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        return ""

    box_x, box_y = 36, 84
    box_w, box_h = 400, 492
    
    step_x = box_w / target_cols
    step_y = box_h / target_rows

    svg_rows = []

    # Row-by-row grouping prevents the browser from freezing
    for y in range(target_rows):
        row_circles = []
        for x in range(target_cols):
            # Extract true RGB values
            r_val, g_val, b_val = pixels[x, y]
            
            # Calculate brightness to filter out the background
            brightness = (r_val + g_val + b_val) / (3.0 * 255.0)
            
            # Skip pure white/very light background pixels
            if brightness > 0.95:
                continue

            target_cx = round(box_x + (x * step_x) + (step_x / 2), 2)
            target_cy = round(box_y + (y * step_y) + (step_y / 2), 2)
            
            # FIXED: Constant slightly larger radius (1.7) so dots overlap. 
            # This creates a solid, clear image where details don't wash out into the background!
            radius = 1.7 
            color = f"rgb({r_val},{g_val},{b_val})"

            row_circles.append(f'<circle cx="{target_cx}" cy="{target_cy}" r="{radius}" fill="{color}"/>')

        if row_circles:
            # Cascading delay: smooth waterfall effect
            delay = round(0.2 + (y * 0.015), 3)
            row_group = f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="{delay}s" fill="freeze"/>' + "".join(row_circles) + '</g>'
            svg_rows.append(row_group)

    return "\n".join(svg_rows)

def update_svg_files():
    image_path = os.path.join("logos", "profile.png")
    print(f"Reading portrait source from {image_path}...")
    
    portrait_group = generate_dot_portrait_svg(image_path)
    
    if not portrait_group:
        print("Error: Portrait generation failed. Please check logos/profile.png.")
        return

    # ---------------------------------------------------------
    # DARK THEME (Sleek Terminal with Light Pink & Glitter)
    # ---------------------------------------------------------
    dark_svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1180" height="610" viewBox="0 0 1180 610" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Bandi H V S S Bhavya">
  <defs>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFB6C1" stop-opacity="0"/>
      <stop offset="50%" stop-color="#FFB6C1" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#FFB6C1" stop-opacity="0"/>
    </linearGradient>
    <filter id="glowPink" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
    <filter id="sparkleGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.5"/></filter>
    <clipPath id="winClip"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath>
    <clipPath id="photoClip"><rect x="36" y="84" width="400" height="492" rx="10"/></clipPath>
  </defs>

  <rect x="2" y="2" width="1176" height="606" rx="18" fill="#0A0A0A"/>
  <g clip-path="url(#winClip)">
    <rect x="2" y="2" width="1176" height="606" fill="#0F0F0F"/>
    <rect x="2" y="2" width="1176" height="46" fill="#141414"/>
    <line x1="2" y1="48" x2="1178" y2="48" stroke="rgba(255,182,193,0.2)"/>
    
    <circle cx="30" cy="25.0" r="5.5" fill="#ff5f56"/>
    <circle cx="50" cy="25.0" r="5.5" fill="#ffbd2e"/>
    <circle cx="70" cy="25.0" r="5.5" fill="#27c93f"/>
    <text x="590.0" y="29.0" text-anchor="middle" font-size="12" fill="#FFB6C1">bandihemavenkatasaisribhavya@gmail.com - % ./profile.sh --live</text>

    <text x="38" y="74" font-size="10" letter-spacing="3" fill="#FFB6C1" opacity="0.8">VISUAL.MAP</text>
    <rect x="36" y="84" width="400" height="492" rx="10" fill="#050505" stroke="rgba(255,182,193,0.3)" stroke-width="1.5"/>

    <g fill="#FFB6C1" filter="url(#sparkleGlow)">
      <text x="55" y="110" font-size="16">✦<animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/></text>
      <text x="410" y="130" font-size="12">✧<animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/></text>
      <text x="380" y="450" font-size="14">✦<animate attributeName="opacity" values="0.3;0.9;0.3" dur="2.5s" repeatCount="indefinite"/></text>
      <text x="50" y="520" font-size="15">✧<animate attributeName="opacity" values="0.8;0.2;0.8" dur="1.8s" repeatCount="indefinite"/></text>
    </g>

    <g clip-path="url(#photoClip)">
      <g id="portrait">
        {portrait_group}
      </g>
      <rect x="36" y="84" width="400" height="12" fill="url(#scanGrad)">
        <animate attributeName="y" values="84;564;84" dur="3s" repeatCount="indefinite"/>
      </rect>
    </g>

    <rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="#FF69B4" stroke-width="2" opacity="0.6" filter="url(#glowPink)">
      <animate attributeName="stroke-opacity" values="0.3;0.9;0.3" dur="3s" repeatCount="indefinite"/>
    </rect>

    <text x="470" y="106" font-size="13" letter-spacing="2" fill="#FFB6C1" font-weight="700">SYSTEM.INFO</text>
    <line x1="566" y1="102" x2="1061" y2="102" stroke="rgba(255,182,193,0.2)"/>
    <text x="1125" y="106" text-anchor="end" font-size="12" fill="#FF69B4" font-weight="700"><tspan>&#9679;</tspan> LIVE<animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/></text>

    <!-- PERFECTLY CASCADING TEXT ANIMATIONS -->
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.8s" fill="freeze"/>
      <rect x="470" y="122" width="310" height="20" rx="4" fill="rgba(255,182,193,0.15)"/>
      <text x="479" y="136" font-size="12" font-weight="700" fill="#FFB6C1">bandihemavenkatasaisribhavya@gmail.com</text>
      <line x1="790" y1="130" x2="1125" y2="130" stroke="rgba(255,182,193,0.2)"/>
    </g>

    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.1s" fill="freeze"/><text x="470" y="162" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Subject </tspan><tspan fill="rgba(255,182,193,0.2)">.....................................</tspan><tspan fill="#FFFFFF" font-weight="600"> BANDI H V S S BHAVYA</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.3s" fill="freeze"/><text x="470" y="188" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Origin </tspan><tspan fill="rgba(255,182,193,0.2)">......................................</tspan><tspan fill="#FFFFFF" font-weight="600"> NIT Jalandhar / Rajamahendravaram</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.5s" fill="freeze"/><text x="470" y="214" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Education </tspan><tspan fill="rgba(255,182,193,0.2)">...................................</tspan><tspan fill="#FFFFFF" font-weight="600"> B.Tech in CSE (2022-2026)</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.7s" fill="freeze"/><text x="470" y="240" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Status </tspan><tspan fill="rgba(255,182,193,0.2)">...................................</tspan><tspan fill="#FFFFFF" font-weight="600"> Built InterviewNovaAI &amp; DataPulse AI</tspan></text></g>
    
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.9s" fill="freeze"/><text x="470" y="266" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">ToolChain </tspan><tspan fill="rgba(255,182,193,0.2)">................................</tspan><tspan fill="#FFFFFF" font-weight="600"> Git, GitHub, VS Code, Docker, Supabase</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.1s" fill="freeze"/><text x="470" y="297" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Core.Lang </tspan><tspan fill="rgba(255,182,193,0.2)">................................</tspan><tspan fill="#FFFFFF" font-weight="600"> Python, Java, C, C++, JavaScript, TypeScript</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.3s" fill="freeze"/><text x="470" y="323" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Core.Frontend </tspan><tspan fill="rgba(255,182,193,0.2)">............................</tspan><tspan fill="#FFFFFF" font-weight="600"> React, Vite, Tailwind CSS, HTML5, CSS3</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.5s" fill="freeze"/><text x="470" y="349" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Core.Backend </tspan><tspan fill="rgba(255,182,193,0.2)">.............................</tspan><tspan fill="#FFFFFF" font-weight="600"> Node.js, Express.js, REST APIs</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.7s" fill="freeze"/><text x="470" y="375" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Core.Database </tspan><tspan fill="rgba(255,182,193,0.2)">............................</tspan><tspan fill="#FFFFFF" font-weight="600"> MySQL, PostgreSQL, MongoDB, DBMS</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.9s" fill="freeze"/><text x="470" y="401" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Core.AI </tspan><tspan fill="rgba(255,182,193,0.2)">..................................</tspan><tspan fill="#FFFFFF" font-weight="600"> Groq AI, Recharts, Data Analysis</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="3.1s" fill="freeze"/><text x="470" y="431" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">- Contact </tspan><tspan fill="rgba(255,182,193,0.2)">---------------------------------------------------------------------</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="3.3s" fill="freeze"/><text x="470" y="454" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Grid.Mail </tspan><tspan fill="rgba(255,182,193,0.2)">................................</tspan><tspan fill="#FFFFFF" font-weight="600"> bandihemavenkatasaisribhavya@gmail.com</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="3.5s" fill="freeze"/><text x="470" y="477" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Grid.Phone </tspan><tspan fill="rgba(255,182,193,0.2)">...............................</tspan><tspan fill="#FFFFFF" font-weight="600"> +91 9059428659</tspan></text></g>
    
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="3.7s" fill="freeze"/>
      <a href="https://www.linkedin.com/in/bandi-hema-venkata-sai-sri-bhavya-6b188328b/" target="_blank">
        <text x="470" y="500" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Grid.LinkedIn </tspan><tspan fill="rgba(255,182,193,0.2)">............................</tspan><tspan fill="#FFB6C1" font-weight="600"> bandi-hema-venkata-sai-sri-bhavya-6b188328b</tspan></text>
      </a>
    </g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="3.9s" fill="freeze"/>
      <a href="https://github.com/BandiHemaVenkataSaiSriBhavya" target="_blank">
        <text x="470" y="523" font-size="14" xml:space="preserve"><tspan fill="#FFB6C1">Grid.GitHub </tspan><tspan fill="rgba(255,182,193,0.2)">..............................</tspan><tspan fill="#FFB6C1" font-weight="600"> BandiHemaVenkataSaiSriBhavya</tspan></text>
      </a>
    </g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="4.2s" fill="freeze"/>
      <text x="470" y="577" font-size="14" fill="#FFB6C1">&#9656; Check out my projects and experience below in README &#8595; <tspan fill="#FF69B4">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
    </g>
  </g>
  <rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="#FF69B4" stroke-width="1.6"/>
</svg>"""

    # ---------------------------------------------------------
    # LIGHT THEME (Perfected High-Contrast Logic)
    # Replaces backgrounds with bright tones and all text/lines 
    # with deep Burgundy and Magenta so NOTHING gets lost.
    # ---------------------------------------------------------
    light_svg_content = dark_svg_content.replace(
        "#0A0A0A", "#FDF2F8"         # Outer background (Tailwind Pink-50)
    ).replace(
        "#0F0F0F", "#FCE7F3"         # Inner terminal background (Pink-100)
    ).replace(
        "#141414", "#FBCFE8"         # Terminal header (Pink-200)
    ).replace(
        "#050505", "#FFFFFF"         # Portrait Box background (Pure White)
    ).replace(
        "#FFFFFF", "#4A0023"         # White values -> Deep Burgundy (High contrast!)
    ).replace(
        "#FFB6C1", "#BE185D"         # Light Pink text -> Dark Magenta
    ).replace(
        "#FF69B4", "#9D174D"         # Hot Pink accents -> Darker Pink 
    ).replace(
        "rgba(255,182,193,0.3)", "rgba(157,23,77,0.3)"  # Adjust borders
    ).replace(
        "rgba(255,182,193,0.2)", "rgba(157,23,77,0.2)"  # Adjust grid lines
    ).replace(
        "rgba(255,182,193,0.15)", "rgba(157,23,77,0.1)" # Adjust label background
    )

    with open("dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg_content)
    
    with open("light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg_content)
    
    print("✓ Successfully generated optimized, true-color portraits with perfectly readable light & dark themes!")

if __name__ == "__main__":
    update_svg_files()