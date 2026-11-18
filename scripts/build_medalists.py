import json
import os
from pathlib import Path

def main():
    # Resolve paths relative to this script
    script_dir = Path(__file__).parent
    data_path = script_dir / "../data/medalists.json"
    html_path = script_dir / "../medalists.html"

    # Read JSON data
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            medalists = json.load(f)
    except Exception as e:
        print(f"Error reading {data_path}: {e}")
        return

    # Group by year (newest first) and preserve order within each year
    groups = {}
    for entry in sorted(medalists, key=lambda x: -x['year']):
        year = str(entry['year'])
        if year not in groups:
            groups[year] = []
        groups[year].append(entry)

    # Read and validate HTML template
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading {html_path}: {e}")
        return

    # Find the generated block markers
    start_marker = "<!-- BEGIN GENERATED MEDALISTS -->"
    end_marker = "<!-- END GENERATED MEDALISTS -->"

    if html_content.count(start_marker) != 1 or html_content.count(end_marker) != 1:
        print(f"Error: Missing or duplicated marker in {html_path}")
        return

    # Generate the new medalist content
    generated_html = ""
    for year, entries in sorted(groups.items(), key=lambda x: -int(x[0])):
        group_content = f"<section class=\"year-group\" data-year="{year}">"
        group_content += f"<h2>{year}</h2><ul>"

        for entry in entries:
            name = entry['name']
            status = entry.get('status')
            if status == "declined":
                name += " (declined the medal)"
            group_content += f"<li>{name}</li>"

        group_content += "</ul></section>"
        generated_html += group_content

    # Replace only the marked block in the HTML file
    new_html = html_content.replace(start_marker, generated_html, 1).replace(end_marker, "", 1)

    # Write back to medalists.html
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_html)
    except Exception as e:
        print(f"Error writing {html_path}: {e}")
        return

    # Verification output
    print(f"Generated {len(groups)} year groups containing {sum(len(v) for v in groups.values())} medalists")

if __name__ == "__main__":
    main()
