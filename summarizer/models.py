#  Video, Transcript and Summary models.

from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=11, primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.video_id})"


class Transcript(models.Model):
    video = models.OneToOneField(Video, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcript for {self.video.video_id}"


class Summary(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="summaries")
    # In Phase 1, we will uncomment and link this to a user
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    summary_text = models.TextField()
    formatted_summary_text = models.TextField()
    model_used = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.video.video_id} by {self.model_used}"
