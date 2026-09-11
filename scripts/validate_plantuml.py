import re
import sys
import subprocess
import os
import tempfile

def extract_plantuml(content):
    # Regex to find ::plant-uml blocks with or without attributes like {alt="..."}
    pattern = re.compile(r'::plant-uml(?:\{[^}]*\})?\s+```plantuml\s+(.*?)```\s+::', re.DOTALL)
    return pattern.findall(content)

def validate_plantuml(code):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name
    
    try:
        # Use --check-syntax to validate
        result = subprocess.run(['plantuml', '--check-syntax', tmp_path], 
                                capture_output=True, text=True)
        if result.returncode != 0:
            return result.stdout or result.stderr
        return None
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_plantuml.py <file.md>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = extract_plantuml(content)
    if not blocks:
        print("No PlantUML blocks found.")
        return

    errors = []
    for i, code in enumerate(blocks):
        error = validate_plantuml(code)
        if error:
            errors.append(f"Block {i+1}:\nCode:\n{code}\nError:\n{error}")
    
    if errors:
        print("\n--- Syntax Errors Found ---\n")
        for err in errors:
            print(err)
            print("-" * 20)
        sys.exit(1)
    else:
        print("All PlantUML blocks are valid.")

if __name__ == "__main__":
    main()
