import re

def on_page_markdown(markdown, **kwargs):
    # Replace <!-- youtube: VIDEO_ID --> with iframe
    pattern = r'<!-- youtube:\s*([\w-]+)\s*-->'
    
    def replace_video(match):
        video_id = match.group(1)
        return f'''<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
  <iframe 
    src="https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1&controls=1&rel=0" 
    frameborder="0" 
    allowfullscreen
    allow="autoplay; encrypted-media"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
  </iframe>
</div>'''
    
    return re.sub(pattern, replace_video, markdown)