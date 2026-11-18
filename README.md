# fieldsmedal.org

## Content Management

All structured data lives in the `data/` directory. To update medalist information:
1. Edit `data/medalists.json`
2. Run the generator:
   python scripts/build_medalists.py
3. Commit the regenerated HTML file along with any JSON changes.

This keeps our source of truth in JSON while ensuring generated pages stay up to date.