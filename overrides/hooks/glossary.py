import re
from pathlib import Path

def on_page_markdown(markdown, page, config, files):
    """
    Process snippet includes before markdown rendering
    """
    docs_dir = Path(config['docs_dir'])
    page_path = Path(page.file.src_path).parent
    
    # Pattern to match --8<-- "path:snippet"
    pattern = r'--8<--\s+"([^"]+):([^"]+)"'
    
    def replace_snippet(match):
        file_path = match.group(1)
        snippet_name = match.group(2)
        
        # Resolve relative path from page location
        full_path = (docs_dir / page_path / file_path).resolve()
        
        if not full_path.exists():
            return f"*Snippet file not found: {file_path}*"
        
        content = full_path.read_text()
        
        # Extract snippet
        snippet_pattern = rf'<!-- snippet: {snippet_name} -->(.*?)<!-- endsnippet -->'
        snippet_match = re.search(snippet_pattern, content, re.DOTALL)
        
        if snippet_match:
            return snippet_match.group(1).strip()
        
        return f"*Snippet '{snippet_name}' not found*"
    
    return re.sub(pattern, replace_snippet, markdown)