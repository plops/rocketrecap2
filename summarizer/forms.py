# Django form for the UI

from django import forms

class SummarizerForm(forms.Form):
    GEMINI_MODELS = [
        ("gemini-1.5-pro-latest", "Gemini 1.5 Pro"),
        ("gemini-1.5-flash-latest", "Gemini 1.5 Flash"),
    ]

    youtube_url = forms.URLField(
        label="YouTube Video URL",
        widget=forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=...'}),
        required=True,
    )
    model = forms.ChoiceField(
        choices=GEMINI_MODELS,
        label="Select AI Model",
        required=True,
    )

