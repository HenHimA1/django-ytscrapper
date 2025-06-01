import json
import requests
from django.contrib import admin, messages
from pytubefix import YouTube
from .models import YouTubeVideo, ParaphraseLink, ParaphraseVideo
from import_export.admin import ImportExportMixin

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(ImportExportMixin, admin.ModelAdmin):
    actions = ["download_subtitle", "create_paraphrase"]
    list_filter = ["title", "channel_url"]
    list_display = ('url', 'title', 'views', 'uploaded_at')
    search_fields = ('url', 'title')
    ordering = ["-views"]

    def create_paraphrase(modeladmin, request, queryset):
        for record in queryset:
            if not record.subtitle: continue
            responses = []
            try:
                url = ParaphraseLink.objects.all()[0].url
                response = requests.post(url=url, 
                                         headers={"Content-Type": "application/json"}, 
                                         data=json.dumps({"content": record.subtitle,
                                                          "yt_id": record.id}))
                responses.append(f"{record.id} : {response.status_code}")
            except Exception as e:
                modeladmin.message_user(request, f"Failed {record.url}: {e}", level=messages.ERROR)
        modeladmin.message_user(request, ", ".join(responses), level=messages.SUCCESS)
    
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
        modeladmin.message_user(request, "Download complete", level=messages.SUCCESS)

@admin.register(ParaphraseVideo)
class ParaphraseVideoAdmin(admin.ModelAdmin):
    search_fields = ['title', 'tags']
    list_display = ["title", "category", "tags"]

@admin.register(ParaphraseLink)
class ParaphraseLinkAdmin(admin.ModelAdmin):
    list_display = ["url"]