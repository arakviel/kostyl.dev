import re
import sys

def clean_for_tts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Docus components containers (::name and ::)
    content = re.sub(r'::[a-z-]+\n', '', content)
    content = re.sub(r'\n::', '', content)
    
    # 2. Remove mermaid blocks
    content = re.sub(r'```mermaid[\s\S]*?```', '', content)
    
    # 3. Remove other code blocks if any (usually not good for TTS unless requested)
    # But for this file, let's keep them if they are small or relevant, 
    # but the user said "without extra constructions". 
    # Let's remove all code blocks.
    content = re.sub(r'```[\s\S]*?```', '', content)
    
    # 4. Remove images ![]()
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    
    # 5. Remove horizontal rules ---
    content = re.sub(r'\n---\n', '\n', content)
    
    # 6. Remove Docus labels like #title and #content
    content = re.sub(r'#title\n', '', content)
    content = re.sub(r'#content\n', '', content)
    
    # 7. Remove markdown formatting but keep text
    # Headers #
    content = re.sub(r'^#+ ', '', content, flags=re.MULTILINE)
    # Bold/Italic ** or * or _
    content = re.sub(r'(\*\*|\*|_)', '', content)
    # Links [text](url) -> text
    content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content)
    # Blockquotes >
    content = re.sub(r'^> ', '', content, flags=re.MULTILINE)
    
    # 8. Clean up extra newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python clean_tts.py <input_md> <output_txt>")
        sys.exit(1)
    
    cleaned = clean_for_tts(sys.argv[1])
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"Cleaned text saved to {sys.argv[2]}")
