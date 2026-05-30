import markdown
import re
import argparse
import sys
from pathlib import Path

def build_site(readme_path='README.md', output='index.html', repo_url=None):
    # 1. Read README
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {readme_path}")
        sys.exit(1)

    # 2. Extract title from first # heading and remove it from body
    title = "My Awesome Project"
    lines = md_text.splitlines()
    new_lines = []
    found_title = False
    for line in lines:
        if not found_title and line.startswith('# '):
            title = line[2:].strip()
            found_title = True
            continue
        new_lines.append(line)
    md_text = '\n'.join(new_lines)

    # 3. Extract shields.io badges
    badge_pattern = r'!\[.*?\]\((https://img\.shields\.io/[^\)]+)\)'
    badges = re.findall(badge_pattern, md_text)
    badges_html = ''
    if badges:
        badges_html = '<div class="badges">' + ''.join(
            f'<img src="{b}" alt="badge">' for b in badges
        ) + '</div>'

    # 4. Convert markdown to HTML
    html_body = markdown.markdown(md_text, extensions=['extra', 'codehilite'])

    # 5. Repository quick-link buttons
    github_buttons_html = ''
    if repo_url:
        buttons = [
            ('📄', 'Issues', f'https://github.com/{repo_url}/issues'),
            ('🔀', 'Pull Requests', f'https://github.com/{repo_url}/pulls'),
            ('📦', 'Releases', f'https://github.com/{repo_url}/releases'),
            ('📖', 'Wiki', f'https://github.com/{repo_url}/wiki'),
            ('⭐', 'Star', f'https://github.com/{repo_url}'),
        ]
        github_buttons_html = '\n'.join(
            f'<a class="gh-btn" href="{link}" target="_blank">{icon} {label}</a>'
            for icon, label, link in buttons
        )

    # 6. Build the full HTML page
    html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- فونت Inter از گوگل -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #f8fafc;
            --text: #1e293b;
            --text-secondary: #475569;
            --primary: #3b82f6;
            --primary-dark: #2563eb;
            --border: #e2e8f0;
            --code-bg: #f1f5f9;
            --card-bg: rgba(255, 255, 255, 0.75);
            --glass-border: rgba(255, 255, 255, 0.5);
            --shadow: 0 8px 32px rgba(0,0,0,0.08);
            --radius: 20px;
            --gradient-1: #fbc2eb;
            --gradient-2: #a6c1ee;
            --gradient-3: #c2e9fb;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg: #0f172a;
                --text: #e2e8f0;
                --text-secondary: #94a3b8;
                --primary: #818cf8;
                --primary-dark: #6366f1;
                --border: #334155;
                --code-bg: #1e293b;
                --card-bg: rgba(15, 23, 42, 0.75);
                --glass-border: rgba(255, 255, 255, 0.1);
                --shadow: 0 8px 32px rgba(0,0,0,0.6);
                --gradient-1: #4f46e5;
                --gradient-2: #7c3aed;
                --gradient-3: #a78bfa;
            }}
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            line-height: 1.7;
            color: var(--text);
            min-height: 100vh;
            animation: fadeIn 0.8s ease-out;
            background: var(--bg);
            overflow-x: hidden;
            position: relative;
        }}

        body::before {{
            content: "";
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(217deg, var(--gradient-1), var(--gradient-2), var(--gradient-3));
            background-size: 600% 600%;
            animation: waveMove 20s ease infinite;
            z-index: -2;
            opacity: 0.35;
            filter: blur(100px);
        }}

        body::after {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: conic-gradient(from 0deg, var(--gradient-2), var(--gradient-3), var(--gradient-1), var(--gradient-2));
            background-size: 200% 200%;
            animation: rotateHue 30s linear infinite;
            z-index: -1;
            opacity: 0.2;
            mix-blend-mode: overlay;
        }}

        @keyframes waveMove {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes rotateHue {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .hero {{
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--glass-border);
            padding: 4rem 1.5rem 3rem;
            text-align: center;
            margin-bottom: -1px;
            box-shadow: var(--shadow);
        }}

        .hero h1 {{
            font-size: 3.8rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }}

        .hero .badges {{
            margin: 1.5rem 0 0.5rem;
        }}

        .hero .badges img {{
            margin: 0.25rem;
        }}

        #github-stats {{
            margin-top: 1.8rem;
            display: flex;
            justify-content: center;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}

        .gh-btn {{
            background: var(--primary);
            color: white;
            padding: 0.65rem 1.5rem;
            border-radius: 2rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            display: inline-block;
            font-size: 0.95rem;
            letter-spacing: 0.3px;
            font-family: 'Inter', sans-serif;
        }}

        .gh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
            background: var(--primary-dark);
        }}

        .container {{
            max-width: 820px;
            margin: 0 auto;
            padding: 1rem 1.5rem 3rem;
            position: relative;
            z-index: 1;
        }}

        main {{
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 2.5rem;
            margin-top: 2rem;
        }}

        main h1, main h2, main h3 {{
            margin-top: 2rem;
            margin-bottom: 0.8rem;
            font-weight: 700;
            color: var(--primary);
            font-family: 'Inter', sans-serif;
        }}

        main h1 {{ font-size: 2rem; border-bottom: 2px solid var(--primary); padding-bottom: 0.4rem; }}
        main h2 {{ font-size: 1.6rem; }}
        main h3 {{ font-size: 1.3rem; }}

        main p {{
            margin-bottom: 1.2rem;
            font-family: 'Inter', sans-serif;
        }}

        main a {{
            color: var(--primary);
            text-decoration: none;
            border-bottom: 1px dashed var(--primary);
            transition: 0.2s;
            font-family: 'Inter', sans-serif;
        }}

        main a:hover {{
            border-bottom-style: solid;
            color: var(--primary-dark);
        }}

        pre {{
            background: var(--code-bg);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.2rem;
            overflow-x: auto;
            margin: 1.5rem 0;
            font-size: 0.95rem;
        }}

        code {{
            font-family: 'Cascadia Code', 'Fira Code', monospace;
            background: var(--code-bg);
            padding: 0.2em 0.4em;
            border-radius: 6px;
            font-size: 0.9em;
        }}

        pre code {{
            background: transparent;
            padding: 0;
        }}

        blockquote {{
            border-left: 4px solid var(--primary);
            padding: 0.5rem 1.5rem;
            margin: 1.5rem 0;
            color: var(--text-secondary);
            font-style: italic;
            background: var(--code-bg);
            border-radius: 0 8px 8px 0;
        }}

        img {{
            max-width: 100%;
            border-radius: var(--radius);
            margin: 1.5rem 0;
            box-shadow: var(--shadow);
        }}

        footer {{
            text-align: center;
            margin-top: 4rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-family: 'Inter', sans-serif;
        }}

        footer a {{
            color: var(--primary);
            text-decoration: none;
        }}

        @media (max-width: 600px) {{
            .hero h1 {{ font-size: 2.5rem; }}
            main {{ padding: 1.5rem; }}
        }}
    </style>
</head>
<body>
    <header class="hero">
        <h1>{title}</h1>
        <div id="github-stats">
            {github_buttons_html}
        </div>
    </header>
    <div class="container">
        <main>
            {html_body}
        </main>
        <footer>
            <p>Built with 🦚 <a href="https://github.com/ZvanTors/readme-peacock" target="_blank">readme-peacock</a></p>
        </footer>
    </div>
</body>
</html>"""

    # 7. Write output file
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html_page)

    print(f"✅ Landing page created for '{title}': {output}")

def main():
    parser = argparse.ArgumentParser(description='🦚 readme-peacock: Beautiful landing page from README.md')
    parser.add_argument('input', nargs='?', default='README.md', help='Path to README.md')
    parser.add_argument('-o', '--output', default='index.html', help='Output HTML file')
    parser.add_argument('--repo', help='GitHub repository "user/repo" for quick-link buttons')
    parser.add_argument('-v', '--version', action='version', version='readme-peacock 1.0.1')
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)

    build_site(args.input, args.output, args.repo)

if __name__ == "__main__":
    main()