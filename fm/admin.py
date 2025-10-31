from django.contrib import admin

from .models import (
    Gallery, GalleryImage, MediaFile, NewsPost, Page, SiteLogo, Slider, TeamMember,
    ProgramSchedule, ArchiveProgram, ContactMessage
)

admin.site.register(MediaFile)

# fm/admin.py

@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ['logo']
    fields = ['logo']

    def has_add_permission(self, request):
        # Allow only ONE instance
        return not SiteLogo.objects.exists()

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at', 'is_published']
    list_filter = ['is_published', 'published_at']
    search_fields = ['title', 'subtitle']
    prepopulated_fields = {'title': ('title',)}  # optional
    date_hierarchy = 'published_at'

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'title': ('slug',)}  # Auto-fill title from slug

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'category']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(ProgramSchedule)
class ProgramScheduleAdmin(admin.ModelAdmin):
    list_display = ['program_name', 'get_day_display', 'start_time', 'end_time']
    list_filter = ['day']

@admin.register(ArchiveProgram)
class ArchiveProgramAdmin(admin.ModelAdmin):
    list_display = ['program_name', 'broadcast_date']
    list_filter = ['broadcast_date']
    search_fields = ['program_name']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'submitted_at']
    readonly_fields = ['submitted_at']
    search_fields = ['name', 'email']

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image', 'order']  
    list_editable = ['order']

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'caption']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    list_display = ['title', 'created_at']