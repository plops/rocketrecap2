# Django form for the UI

from django import forms

class SummarizerForm(forms.Form):
    GEMINI_MODELS = [
        ("gemini-2.5-flash", "Gemini 2.5 Flash"),
        ("gemini-2.5-pro", "Gemini 2.5 Pro"),
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

