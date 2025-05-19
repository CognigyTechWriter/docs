import os
import json
from pathlib import Path

def load_docs_json():
    with open('docs.json', 'r') as f:
        return json.load(f)

def extract_paths_from_docs(data, prefix='docs/ai'):
    paths = set()
    
    def extract_from_dropdown(dropdown):
        if 'pages' in dropdown:
            for page in dropdown['pages']:
                if isinstance(page, str):
                    if page.startswith(prefix):
                        paths.add(page)
                elif isinstance(page, dict):
                    if 'pages' in page:
                        extract_from_dropdown(page)
    
    for dropdown in data.get('navigation', {}).get('dropdowns', []):
        extract_from_dropdown(dropdown)
    
    return paths

def get_actual_files(start_paths=['docs/ai', 'docs/ai-copilot']):
    actual_files = set()
    for start_path in start_paths:
        for root, _, files in os.walk(start_path):
            for file in files:
                if file.endswith('.mdx'):
                    # Convert to relative path and remove .mdx extension
                    rel_path = os.path.join(root, file)
                    rel_path = rel_path[:-4]  # Remove .mdx extension
                    actual_files.add(rel_path)
    return actual_files

def main():
    # Load docs.json
    docs_data = load_docs_json()
    
    # Extract paths from docs.json
    docs_paths = extract_paths_from_docs(docs_data)
    
    # Get actual files in the repository
    actual_files = get_actual_files()
    
    # Find discrepancies
    missing_files = docs_paths - actual_files
    extra_files = actual_files - docs_paths
    
    # Print results
    print("\n=== Path Verification Results ===\n")
    
    print("Files in docs.json but not in repository:")
    for path in sorted(missing_files):
        print(f"  - {path}")
    
    print("\nFiles in repository but not in docs.json:")
    for path in sorted(extra_files):
        print(f"  + {path}")
    
    print(f"\nTotal files in docs.json: {len(docs_paths)}")
    print(f"Total files in repository: {len(actual_files)}")
    print(f"Missing files: {len(missing_files)}")
    print(f"Extra files: {len(extra_files)}")

if __name__ == "__main__":
    main() 