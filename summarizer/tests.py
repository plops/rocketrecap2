#  unit tests for utils.

from django.test import TestCase
from .utils import validate_youtube_url, convert_markdown_to_youtube_format


class UtilsTestCase(TestCase):
    def test_validate_youtube_url(self):
        self.assertEqual(
            "0123456789a",
            validate_youtube_url("https://www.youtube.com/live/0123456789a"),
        )
        self.assertEqual(
            "0123456789a",
            validate_youtube_url("https://www.youtube.com/live/0123456789a&abc=123"),
        )
        self.assertEqual(
            "_123456789a",
            validate_youtube_url("https://www.youtube.com/watch?v=_123456789a&abc=123"),
        )
        self.assertEqual(
            "_123456789a",
            validate_youtube_url("https://youtube.com/watch?v=_123456789a&abc=123"),
        )
        self.assertEqual(
            "-123456789a",
            validate_youtube_url("https://www.youtu.be/-123456789a&abc=123"),
        )
        self.assertEqual(
            "-123456789a", validate_youtube_url("https://youtu.be/-123456789a&abc=123")
        )
        self.assertFalse(
            validate_youtube_url("http://www.youtube.com/live/0123456789a")
        )  # not https
        self.assertFalse(validate_youtube_url("https://example.com"))

    def test_convert_markdown_to_youtube_format(self):
        text = r"""**Title:**
Let's **go** to http://www.google.com/search?q=hello."""
        expected = r"""*Title:*
Let's *go* to http://www.google-dot-com/search?q=hello."""
        self.assertEqual(expected, convert_markdown_to_youtube_format(text))


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
    lines = vtt_content_string.strip().split("\n")
    captions = webvtt.read_buffer(iter(lines))

    output = []
    last_text = None
    for caption in captions:
        # Simple deduplication
        if caption.text != last_text:
            timestamp = caption.start.split(".")[0]  # Remove milliseconds
            text = caption.text.replace("\n", " ").strip()
            output.append(f"{timestamp} {text}")
            last_text = caption.text

    return "\n".join(output)


def convert_markdown_to_youtube_format(text):
    """Adapts markdown for YouTube comments."""
    text = text.replace("**:", ":**").replace("**,", ",**").replace("**.", " .**")
    text = text.replace("**", "*")
    text = re.sub(r"^##\s*(.*)", r"*\1*", text, flags=re.MULTILINE)
    text = re.sub(
        r"((?:https?:\/\/)?(?:www\.)?\S+)\.(com|org|de|us|gov|net|edu|info|io|co\.uk|ca|fr|au|jp|ru|ch|it|nl|se|es|br|mx|in|kr)",
        r"\1-dot-\2",
        text,
    )
    return text
