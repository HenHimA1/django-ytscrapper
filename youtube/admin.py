from django.contrib import admin
from pytubefix import YouTube
from .models import YouTubeVideo, ParaphraseLink, ParaphraseVideo
from import_export.admin import ImportExportMixin

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(ImportExportMixin, admin.ModelAdmin):
    actions = ["download_subtitle"]
    list_filter = ["title", "channel_url"]
    list_display = ('url', 'title', 'views', 'uploaded_at')
    search_fields = ('url', 'title')
    ordering = ["-uploaded_at"]
    
    def download_subtitle(modeladmin, request, queryset):
        for record in queryset:
            if record.subtitle: continue
            try:
                yt = YouTube(record.url)
                record.title = yt.title
                record.views = yt.views or 0
                record.likes = yt.likes or 0
                record.description = yt.description
                record.channel_url = yt.channel_url 
                record.uploaded_at = yt.publish_date
                record.subtitle = "en" in yt.captions and yt.captions["en"].generate_txt_captions() or "a.en" in yt.captions and yt.captions["a.en"].generate_txt_captions() or ""
                record.save()
            except Exception as e:
                modeladmin.message_user(request, f"Failed {record.url}: {e}")
        modeladmin.message_user(request, "Download complete")

@admin.register(ParaphraseVideo)
class ParaphraseVideoAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "tags"]

@admin.register(ParaphraseLink)
class ParaphraseLinkAdmin(admin.ModelAdmin):
    list_display = ["url"]