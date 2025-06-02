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

    para_title = models.CharField(max_length=100, null=True, blank=True)
    para_content = models.TextField(null=True, blank=True)
    para_tags = models.TextField(null=True, blank=True)
    para_category = models.CharField(max_length=100, null=True, blank=True)
    para_excerpt = models.TextField(null=True, blank=True)
    para_featured_image = models.CharField(max_length=200, null=True, blank=True) 

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Video"
class ParaphraseLink(models.Model):
    url = models.URLField()