# summarizer/utils.py
# utility functions (URL validation, VTT parsing, markdown tweaks).
import re
import webvtt

def validate_youtube_url(url):
    """Validates various YouTube URL formats. Returns the video ID string or False."""
    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:watch\?v=|live\/|embed\/|v\/|shorts\/)([\w-]{11})",
        r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([\w-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return False

def parse_vtt_file(vtt_content_string):
    """Parses VTT content from a string. Returns a formatted transcript string."""
    lines = vtt_content_string.strip().split('\n')
    captions = webvtt.read_buffer(iter(lines))

    output = []
    last_text = None
    for caption in captions:
        # Simple deduplication
        if caption.text != last_text:
            timestamp = caption.start.split('.')[0] # Remove milliseconds
            text = caption.text.replace('\n', ' ').strip()
            output.append(f"{timestamp} {text}")
            last_text = caption.text

    return "\n".join(output)


def convert_markdown_to_youtube_format(text):
    """Adapts markdown for YouTube comments."""
    text = text.replace("**:", ":**").replace("**,", ",**").replace("**."," .**")
    text = text.replace("**", "*")
    text = re.sub(r"^##\s*(.*)", r"*\1*", text, flags=re.MULTILINE)
    text = re.sub(
        r"((?:https?:\/\/)?(?:www\.)?\S+)\.(com|org|de|us|gov|net|edu|info|io|co\.uk|ca|fr|au|jp|ru|ch|it|nl|se|es|br|mx|in|kr)",
        r"\1-dot-\2",
        text,
    )
    return text