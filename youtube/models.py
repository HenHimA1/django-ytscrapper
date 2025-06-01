from django.db import models


class YouTubeVideo(models.Model):
    url = models.URLField("YouTube URL", unique=True)
    title = models.CharField(max_length=255, blank=True)
    channel_url = models.URLField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    subtitle = models.TextField(blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Video"

class CategoryParaphraseVideo(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ParaphraseVideo(models.Model):
    title = models.CharField(max_length=100)
    video = models.ForeignKey(YouTubeVideo, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.TextField()
    category = models.ForeignKey(CategoryParaphraseVideo, blank=True, null=True, on_delete=models.CASCADE)
    excerpt = models.TextField()
    featured_image = models.CharField(max_length=200, null=True, blank=True)

class ParaphraseLink(models.Model):
    url = models.URLField()