# form handling and calling the service.

from django.shortcuts import render
from .forms import SummarizerForm
from .services import generate_and_save_summary, SummaryGenerationError
from .utils import validate_youtube_url

def summarizer_view(request):
    summary = None
    form = SummarizerForm()
    error_message = None

    if request.method == 'POST':
        form = SummarizerForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['youtube_url']
            model_name = form.cleaned_data['model']

            video_id = validate_youtube_url(url)
            if not video_id:
                error_message = "Invalid YouTube URL provided. Please check the link and try again."
            else:
                try:
                    summary = generate_and_save_summary(
                        video_id=video_id,
                        original_url=url,
                        model_name=model_name
                    )
                except SummaryGenerationError as e:
                    error_message = str(e)

    context = {
        'form': form,
        'summary': summary,
        'error_message': error_message,
    }
    return render(request, 'summarizer/summarizer_page.html', context)

