import json
import os
from pathlib import Path
import html

def main():
    # Resolve paths relative to this script
    script_dir = Path(__file__).parent
    data_path = script_dir / "../data/medalists.json"
    medalists_html_path = script_dir / "../medalists.html"
    index_html_path = script_dir / "../index.html"

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

    # Process medalists.html first
    try:
        with open(medalists_html_path, 'r', encoding='utf-8') as f:
            medalists_content = f.read()
    except Exception as e:
        print(f"Error reading {medalists_html_path}: {e}")
        return

    # Validate markers in medalists.html
    start_marker_medalists = "<!-- BEGIN GENERATED MEDALISTS -->"
    end_marker_medalists = "<!-- END GENERATED MEDALISTS -->"

    if medalists_content.count(start_marker_medalists) != 1 or medalists_content.count(end_marker_medalists) != 1:
        print(f"Error: Missing or duplicated marker in {medalists_html_path}")
        return

    start_idx_medalists = medalists_content.find(start_marker_medalists)
    end_idx_medalists = medalists_content.find(end_marker_medal义ists)

    if start_idx_medalists >= end_idx_medalists:
        print(f"Error: Start marker appears after end marker in {medalists_html_path}")
        return

    # Generate medalists content (same as before)
    generated_medalists_html = ""
    for year, entries in sorted(groups.items(), key=lambda x: -int(x[0])):
        group_content = f'<section class="year-group" data-year="{year}">'
        group_content += f"<h2>{year}</h2><ul>"

        for entry in entries:
            name = entry['name']
            status = entry.get('status')
            if status == "declined":
                name += " (declined the medal)"
            escaped_name = html.escape(name)
            group_content += f"<li>{escaped_name}</li>"

        group_content += "</ul></section>"
        generated_medalists_html += group_content

    # Replace content in medalists.html while preserving markers
    before_start_medalists = medalists_content[:start_idx_medalists]
    after_end_medalists = medalists_content[end_idx_medalists + len(end_marker_medalists):]
    new_medalists_html = (
        before_start_medalists + start_marker_medalists + "\n"
        + generated_medalists_html + "\n        " + end_marker_medalists + after_end_medalists
    )

    # Process index.html next
    try:
        with open(index_html_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
    except Exception as e:
        print(f"Error reading {index_html_path}: {e}")
        return

    # Validate markers in index.html
    start_marker_index = "<!-- BEGIN GENERATED LATEST MEDALISTS -->"
    end_marker_index = "<!-- END GENERATED LATEST MEDALISTS -->"

    if index_content.count(start_marker_index) != 1 or index_content.count(end_marker_index) != 1:
        print(f"Error: Missing or duplicated marker in {index_html_path}")
        return

    start_idx_index = index_content.find(start_marker_index)
    end_idx_index = index_content.find(end_marker_index)

    if start_idx_index >= end_idx_index:
        print(f"Error: Start marker appears after end marker in {index_html_path}")
        return

    # Generate latest medalists content from JSON data
    latest_year = next(iter(groups.keys()))  # Get the first (newest) year from sorted groups
    latest_entries = groups[latest_year]

    generated_latest_html = f"<h2>{latest_year}</h2><ul>"
    for entry in latest_entries:
        name = entry['name']
        status = entry.get('status')
        if status == "declined":
            name += " (declined the medal)"
        field = entry.get('field', '')
        summary = entry.get('summary', '')

        escaped_name = html.escape(name)
        escaped_field = html.escape(field) if field else ''
        escaped_summary = html.escape(summary) if summary else ''

        # Add field and summary to the <li> if present
        generated_latest_html += f"<li>{escaped_name}"
        if escaped_field:
            generated_latest_html += f"<br><small>{escaped_field}</small>"
        if escaped_summary:
            generated_latest_html += f"<br><small>{escaped_summary}</small>"
        generated_latest_html += "</li>"

    # Add source link for 2026 citations only
    if latest_year == '2026':
        generated_latest_html += f"<p><a href=\"https://www.mathunion.org/imu-awards/fields-medal/fields-medals-2026\">IMU award citations</a></p>"
    else:
        # Use general IMU link if not 2026
        generated_latest_html += f"<p><a href=\"https://www.mathunion.org/imu-awards/fields-medal\">IMU award citations</a></p>"

    generated_latest_html += "</ul>"

    # Replace content in index.html while preserving markers
    before_start_index = index_content[:start_idx_index]
    after_end_index = index_content[end_idx_index + len(end_marker_index):]
    new_index_html = (
        before_start_index + start_marker_index + "\n"
        + generated_latest_html + "\n        " + end_marker_index + after_end_index
    )

    # Write back to both files (do not write if any error occurred)
    try:
        with open(medalists_html_path, 'w', encoding='utf-8') as f:
            f.write(new_medalists_html)
    except Exception as e:
        print(f"Error writing {medalists_html_path}: {e}")
        return

    try:
        with open(index_html_path, 'w', encoding='utf-8') as f:
            f.write(new_index_html)
    except Exception as e:
        print(f"Error writing {index_html_path}: {e}")
        return

    # Verification output
    print(f"Generated {len(groups)} year groups containing {sum(len(v) for v in groups.values())} medalists")
    print(f"Updated Latest Medalists section with {len(latest_entries)} names from {latest_year}")

if __name__ == "__main__":
    main()