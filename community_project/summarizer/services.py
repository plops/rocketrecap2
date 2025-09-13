# orchestration: download transcript, call Gemini, save summary.

import os
import yt_dlp
from google import genai
from google.genai import types

from .models import Video, Transcript, Summary
from .utils import parse_vtt_file, convert_markdown_to_youtube_format

# Configure the Gemini API client
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class SummaryGenerationError(Exception):
    """Custom exception for errors during summary generation."""
    pass

def _download_transcript(video_id: str) -> str:
    """Downloads the VTT transcript for a given video ID."""
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'outtmpl': f'/tmp/{video_id}', # Use a temporary directory
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'http://www.youtube.com/watch?v={video_id}'])

        vtt_path = f'/tmp/{video_id}.en.vtt'
        if not os.path.exists(vtt_path):
            raise SummaryGenerationError("No English subtitles found for this video.")

        with open(vtt_path, 'r', encoding='utf-8') as f:
            vtt_content = f.read()

        os.remove(vtt_path) # Clean up the file
        return parse_vtt_file(vtt_content)

    except Exception as e:
        print(f"Error downloading transcript: {e}")
        raise SummaryGenerationError(f"Failed to download transcript. Original error: {e}")


def _generate_summary_with_gemini(transcript: str, model_name: str) -> str:
    """Calls the Gemini API to generate a summary."""
    prompt = f"""
    I don't want to watch the video. 
    Based on the following transcript with timestamps, create a self-contained, detailed bullet-point summary that I can understand without watching the video.
    For each major point in the summary, include its starting timestamp from the transcript.

    Transcript:
    {transcript}
    """

    model = genai.GenerativeModel(model_name)

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise SummaryGenerationError(f"Failed to generate summary from the AI model. Original error: {e}")

def generate_and_save_summary(video_id: str, original_url: str, model_name: str) -> Summary:
    """The main service function to orchestrate the summarization process."""

    # 1. Get or create the Video object
    video, created = Video.objects.get_or_create(
        video_id=video_id,
        defaults={'original_url': original_url, 'title': f'Video {video_id}'} # Placeholder title
    )

    # 2. Get or create the Transcript
    try:
        transcript_obj = Transcript.objects.get(video=video)
        transcript_text = transcript_obj.text
    except Transcript.DoesNotExist:
        transcript_text = _download_transcript(video_id)
        Transcript.objects.create(video=video, text=transcript_text)

    # 3. Generate the summary
    raw_summary = _generate_summary_with_gemini(transcript_text, model_name)

    # 4. Format the summary for YouTube
    formatted_summary = convert_markdown_to_youtube_format(raw_summary)

    # 5. Save the summary to the database
    summary = Summary.objects.create(
        video=video,
        summary_text=raw_summary,
        formatted_summary_text=formatted_summary,
        model_used=model_name,
    )

    return summary

