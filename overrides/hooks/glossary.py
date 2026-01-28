import re
from pathlib import Path

def on_page_markdown(markdown, page, config, files):
    """
    Process snippet includes and auto-generate abbreviations for glossary terms
    """
    docs_dir = Path(config['docs_dir'])
    page_path = Path(page.file.src_path).parent
    glossary_path = docs_dir / 'glossary.md'
    
    # Track which terms are used in the page
    used_terms = {}
    
    # Pattern to match --8<-- "path:snippet"
    snippet_pattern = r'--8<--\s+"([^"]+):([^"]+)"'
    
    def replace_snippet(match):
        file_path = match.group(1)
        snippet_name = match.group(2)
        
        # Resolve relative path from page location
        full_path = (docs_dir / page_path / file_path).resolve()
        
        if not full_path.exists():
            return f"*Snippet file not found: {file_path}*"
        
        try:
            content = full_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            return f"*Error reading snippet file {file_path}: {e}*"
        
        # Extract snippet content
        pattern = rf'<!-- snippet: {snippet_name} -->(.*?)<!-- endsnippet -->'
        snippet_match = re.search(pattern, content, re.DOTALL)
        
        if snippet_match:
            snippet_content = snippet_match.group(1).strip()
            
            # Extract term and definition for abbreviations
            # Try to extract acronym and definition from the snippet
            extract_term_from_snippet(snippet_content, used_terms)
            
            return snippet_content
        
        return f"*Snippet '{snippet_name}' not found in {file_path}*"
    
    # Process snippet includes first
    markdown = re.sub(snippet_pattern, replace_snippet, markdown)
    
    # Scan page content for acronyms that match glossary terms
    if glossary_path.exists():
        try:
            glossary_content = glossary_path.read_text(encoding='utf-8')
            scan_for_glossary_terms(markdown, glossary_content, used_terms)
        except Exception as e:
            print(f"Warning: Could not read glossary: {e}")
    
    # Add abbreviations at the end if any terms were found
    if used_terms:
        abbreviations = '\n\n<!-- Auto-generated glossary abbreviations -->\n'
        for term, definition in sorted(used_terms.items()):
            # Clean definition - remove markdown formatting and keep it concise
            clean_def = clean_definition(definition)
            abbreviations += f'*[{term}]: {clean_def}\n'
        markdown += abbreviations
    
    return markdown


def extract_term_from_snippet(snippet_content, used_terms):
    """
    Extract term and definition from a glossary snippet
    """
    # Pattern: ## ACRONYM (Full Name) or ## ACRONYM
    header_pattern = r'^##\s+([A-Z][A-Z0-9-]*(?:/[A-Z]+)?)\s*(?:\(([^)]+)\))?'
    lines = snippet_content.split('\n')
    
    for i, line in enumerate(lines):
        match = re.match(header_pattern, line.strip())
        if match:
            term = match.group(1)
            # Get the definition (next non-empty line after header)
            for j in range(i + 1, len(lines)):
                definition = lines[j].strip()
                if definition and not definition.startswith('#'):
                    used_terms[term] = definition
                    break
            break


def scan_for_glossary_terms(markdown, glossary_content, used_terms):
    """
    Scan the markdown content for acronyms that exist in the glossary
    and haven't been added yet
    """
    # Extract all glossary terms from glossary.md
    glossary_terms = {}
    
    # Find all snippets in glossary
    snippet_pattern = r'<!-- snippet: ([^>]+) -->(.*?)<!-- endsnippet -->'
    for match in re.finditer(snippet_pattern, glossary_content, re.DOTALL):
        snippet_content = match.group(2).strip()
        extract_glossary_term(snippet_content, glossary_terms)
    
    # Find which terms appear in the markdown
    for term, definition in glossary_terms.items():
        # Look for the term as a whole word (not part of another word)
        if re.search(rf'\b{re.escape(term)}\b', markdown) and term not in used_terms:
            used_terms[term] = definition


def extract_glossary_term(snippet_content, glossary_terms):
    """
    Extract term and definition from glossary content
    """
    # Pattern: ## ACRONYM (Full Name) or ## ACRONYM
    header_pattern = r'^##\s+([A-Z][A-Z0-9-]*(?:/[A-Z]+)?)\s*(?:\(([^)]+)\))?'
    lines = snippet_content.split('\n')
    
    for i, line in enumerate(lines):
        match = re.match(header_pattern, line.strip())
        if match:
            term = match.group(1)
            # Get the definition (next non-empty line after header)
            for j in range(i + 1, len(lines)):
                definition = lines[j].strip()
                if definition and not definition.startswith('#'):
                    glossary_terms[term] = definition
                    break
            break


def clean_definition(definition):
    """
    Clean up definition text for abbreviations
    - Remove markdown bold/italic
    - Remove "Application:" section
    - Limit length for tooltips
    """
    # Remove **Application:** section
    definition = re.sub(r'\s*\*\*Application:.*$', '', definition, flags=re.DOTALL)
    
    # Remove markdown formatting
    definition = re.sub(r'\*\*([^*]+)\*\*', r'\1', definition)  # Bold
    definition = re.sub(r'\*([^*]+)\*', r'\1', definition)      # Italic
    definition = re.sub(r'`([^`]+)`', r'\1', definition)        # Code
    
    # Take only first sentence if too long (keep it under ~200 chars for tooltips)
    if len(definition) > 200:
        # Try to cut at first period
        first_sentence = re.match(r'^[^.]+\.', definition)
        if first_sentence:
            definition = first_sentence.group(0)
        else:
            definition = definition[:197] + '...'
    
    return definition.strip()