#!/usr/bin/env python3
import os
import base64

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

def create_banner(is_dark=True, b64_img=""):
    bg_color = "#0B0510" if is_dark else "#FCE7F3"
    panel_bg = "url(#panelGrad)"
    panel_stroke = "rgba(244,114,182,0.4)" if is_dark else "rgba(219,39,119,0.35)"
    text_primary = "#FDF2F8" if is_dark else "#500724"
    text_muted = "#F472B6" if is_dark else "#9D174D"
    header_bar = "#831843" if is_dark else "#FBCFE8"
    header_text = "#FBCFE8" if is_dark else "#831843"
    dot_color = "#F472B6" if is_dark else "#DB2777"

    # Generate matrix vertical rain streams from top to bottom
    matrix_rain = []
    columns = 20
    for col in range(columns):
        x_pos = 50 + (col * 18)
        dur = 3.5 + (col % 4) * 0.7
        delay = (col * 0.25) % 3.0
        matrix_rain.append(
            f'<text x="{x_pos}" y="0" font-size="12" fill="{dot_color}" opacity="0.6">'
            f'1 0 1 0 1 0 1 1 0 1 0 1 0 1 0 1 1 0 1 0 1'
            f'<animate attributeName="y" values="84;576" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.1;0.8;0.1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
            f'</text>'
        )
    rain_svg = "\n".join(matrix_rain)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1180" height="610" viewBox="0 0 1180 610" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace" role="img" aria-label="Bandi Hema Venkata Sai Sri Bhavya">
  <defs>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#EC4899"><animate attributeName="stop-color" values="#EC4899;#F472B6;#D946EF;#EC4899" dur="8s" repeatCount="indefinite"/></stop>
      <stop offset="0.5" stop-color="#F472B6"><animate attributeName="stop-color" values="#F472B6;#D946EF;#EC4899;#F472B6" dur="8s" repeatCount="indefinite"/></stop>
      <stop offset="1" stop-color="#D946EF"><animate attributeName="stop-color" values="#D946EF;#EC4899;#F472B6;#D946EF" dur="8s" repeatCount="indefinite"/></stop>
    </linearGradient>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{dot_color}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{dot_color}" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="{dot_color}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{'#120A16' if is_dark else '#FDF2F8'}"/>
      <stop offset="1" stop-color="{'#1A0D22' if is_dark else '#FCE7F3'}"/>
    </linearGradient>
    <filter id="glowPink" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
    <filter id="sparkleGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.5"/></filter>
    <clipPath id="winClip"><rect x="2" y="2" width="1176" height="606" rx="18"/></clipPath>
    <clipPath id="photoClip"><rect x="36" y="84" width="400" height="492" rx="10"/></clipPath>
  </defs>

  <rect x="2" y="2" width="1176" height="606" rx="18" fill="{bg_color}"/>
  <g clip-path="url(#winClip)">
    <rect x="2" y="2" width="1176" height="606" fill="url(#panelGrad)"/>
    <rect x="2" y="2" width="1176" height="46" fill="{'#180A22' if is_dark else '#FBCFE8'}"/>
    <line x1="2" y1="48" x2="1178" y2="48" stroke="{'rgba(244,114,182,0.15)' if is_dark else 'rgba(219,39,119,0.15)'}"/>
    
    <circle cx="30" cy="25.0" r="5.5" fill="#ff5f56"/>
    <circle cx="50" cy="25.0" r="5.5" fill="#ffbd2e"/>
    <circle cx="70" cy="25.0" r="5.5" fill="#27c93f"/>
    <text x="590.0" y="29.0" text-anchor="middle" font-size="12" fill="{text_muted}">bandihemavenkatasaisribhavya@gmail.com - % ./profile.sh --live</text>

    <text x="38" y="74" font-size="10" letter-spacing="3" fill="{text_muted}" opacity="0.8">VISUAL.MAP</text>
    <rect x="36" y="84" width="400" height="492" rx="10" fill="{'#120A16' if is_dark else '#FDF2F8'}" stroke="{panel_stroke}" stroke-width="1.5"/>

    <g fill="{dot_color}" filter="url(#sparkleGlow)">
      <text x="55" y="110" font-size="16">✦<animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/></text>
      <text x="410" y="130" font-size="12">✧<animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/></text>
    </g>

    <g clip-path="url(#photoClip)">
      <g opacity="0">
        <animate attributeName="opacity" from="0" to="1" dur="0.8s" begin="0.3s" fill="freeze"/>
        <image href="{b64_img}" x="36" y="84" width="400" height="492" preserveAspectRatio="xMidYMid slice">
          <animateTransform attributeName="transform" type="scale" values="1;1.03;1" dur="6s" repeatCount="indefinite" transform-origin="236 330"/>
        </image>
      </g>
      
      <g clip-path="url(#photoClip)" opacity="0.35">
        {rain_svg}
      </g>

      <rect x="36" y="84" width="400" height="12" fill="url(#scanGrad)">
        <animate attributeName="y" values="84;564;84" dur="4s" repeatCount="indefinite"/>
      </rect>
    </g>

    <rect x="36" y="84" width="400" height="492" rx="10" fill="none" stroke="{dot_color}" stroke-width="2" opacity="0.6" filter="url(#glowPink)">
      <animate attributeName="stroke-opacity" values="0.3;0.9;0.3" dur="3s" repeatCount="indefinite"/>
    </rect>

    <text x="470" y="106" font-size="13" letter-spacing="2" fill="{text_muted}" font-weight="700">SYSTEM.INFO</text>
    <line x1="566" y1="102" x2="1061" y2="102" stroke="{'rgba(244,114,182,0.15)' if is_dark else 'rgba(219,39,119,0.15)'}"/>
    <text x="1125" y="106" text-anchor="end" font-size="12" fill="{'#FB7185' if is_dark else '#E11D48'}" font-weight="700"><tspan>&#9679;</tspan> LIVE<animate attributeName="opacity" values="1;0.3;1" dur="1.5s" repeatCount="indefinite"/></text>

    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.6s" fill="freeze"/>
      <rect x="470" y="122" width="310" height="20" rx="4" fill="{header_bar}"/>
      <text x="479" y="136" font-size="12" font-weight="700" fill="{header_text}">bandihemavenkatasaisribhavya@gmail.com</text>
      <line x1="790" y1="130" x2="1125" y2="130" stroke="{'rgba(244,114,182,0.15)' if is_dark else 'rgba(219,39,119,0.15)'}"/>
    </g>

    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="0.90s" fill="freeze"/><text x="470" y="162" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Subject </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">.....................................</tspan><tspan fill="{text_primary}" font-weight="600"> BANDI H V S S BHAVYA</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.02s" fill="freeze"/><text x="470" y="188" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Origin </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">......................................</tspan><tspan fill="{text_primary}" font-weight="600"> NIT Jalandhar / Rajamahendravaram</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.14s" fill="freeze"/><text x="470" y="214" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Education </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">...................................</tspan><tspan fill="{text_primary}" font-weight="600"> B.Tech in CSE (2022-2026)</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.26s" fill="freeze"/><text x="470" y="240" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Status </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">...................................</tspan><tspan fill="{text_primary}" font-weight="600"> Built InterviewNovaAI &amp; DataPulse AI</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.38s" fill="freeze"/><text x="470" y="266" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">ToolChain </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">................................</tspan><tspan fill="{text_primary}" font-weight="600"> Git, GitHub, VS Code, Docker, Supabase</tspan></text></g>

    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.60s" fill="freeze"/><text x="470" y="297" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Core.Lang </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">................................</tspan><tspan fill="{text_primary}" font-weight="600"> Python, Java, C, C++, JavaScript, TypeScript</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.72s" fill="freeze"/><text x="470" y="323" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Core.Frontend </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">............................</tspan><tspan fill="{text_primary}" font-weight="600"> React, Vite, Tailwind CSS, HTML5, CSS3</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.84s" fill="freeze"/><text x="470" y="349" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Core.Backend </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">.............................</tspan><tspan fill="{text_primary}" font-weight="600"> Node.js, Express.js, REST APIs</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="1.96s" fill="freeze"/><text x="470" y="375" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Core.Database </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">............................</tspan><tspan fill="{text_primary}" font-weight="600"> MySQL, PostgreSQL, MongoDB, DBMS</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.08s" fill="freeze"/><text x="470" y="401" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Core.AI </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">..................................</tspan><tspan fill="{text_primary}" font-weight="600"> Groq AI, Recharts, Data Analysis</tspan></text></g>

    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.30s" fill="freeze"/><text x="470" y="431" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">- Contact </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">---------------------------------------------------------------------</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.42s" fill="freeze"/><text x="470" y="454" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Grid.Mail </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">................................</tspan><tspan fill="{text_primary}" font-weight="600"> bandihemavenkatasaisribhavya@gmail.com</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.54s" fill="freeze"/><text x="470" y="477" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Grid.Phone </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">...............................</tspan><tspan fill="{text_primary}" font-weight="600"> +91 9059428659</tspan></text></g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.66s" fill="freeze">
      <a href="https://www.linkedin.com/in/bandi-hema-venkata-sai-sri-bhavya-6b188328b/" target="_blank">
        <text x="470" y="500" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Grid.LinkedIn </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">............................</tspan><tspan fill="{text_muted}" font-weight="600"> bandi-hema-venkata-sai-sri-bhavya-6b188328b</tspan></text>
      </a>
    </g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="2.78s" fill="freeze">
      <a href="https://github.com/BandiHemaVenkataSaiSriBhavya" target="_blank">
        <text x="470" y="523" font-size="14" xml:space="preserve"><tspan fill="{text_muted}">Grid.GitHub </tspan><tspan fill="{'rgba(244,114,182,0.25)' if is_dark else 'rgba(219,39,119,0.2)'}">..............................</tspan><tspan fill="{text_muted}" font-weight="600"> BandiHemaVenkataSaiSriBhavya</tspan></text>
      </a>
    </g>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="3.10s" fill="freeze"/>
      <text x="470" y="577" font-size="14" fill="{text_muted}">&#9656; Check out my projects and experience below in README &#8595; <tspan fill="{dot_color}">&#9608;<animate attributeName="fill-opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
    </g>
  </g>
  <rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="3" opacity="0.65" filter="url(#glowPink)"/>
  <rect x="3" y="3" width="1174" height="604" rx="17" fill="none" stroke="url(#accent)" stroke-width="1.6"/>
</svg>"""

if __name__ == "__main__":
    image_path = os.path.join("logos", "profile.png")
    b64_data = get_base64_image(image_path)
    
    if b64_data:
        with open("dark.svg", "w", encoding="utf-8") as f:
            f.write(create_banner(is_dark=True, b64_img=b64_data))
        print("✓ Successfully generated dark.svg with top-to-bottom matrix rain overlay!")

        with open("light.svg", "w", encoding="utf-8") as f:
            f.write(create_banner(is_dark=False, b64_img=b64_data))
        print("✓ Successfully generated light.svg with top-to-bottom matrix rain overlay!")
    else:
        print("Error: Could not locate logos/profile.png")