from django.contrib import admin
from gallery.models import Album, Tag, Image

# Register your models here.

class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "rating", "size", "tags_", "albums_",
        "thumbnail_", "taken"]
    list_filter = ["tags", "albums"]
    readonly_fields =["thumbnail_", "size",]

    def save_model(self, request, obj, form, change):
        obj.save()


admin.site.register(Album, AlbumAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)