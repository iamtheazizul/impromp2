from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=250)
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title


class VideoAnalysis(models.Model):
    video = models.ForeignKey(
        Video, related_name='analyses', on_delete=models.CASCADE)
    analysis_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.video.title} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
