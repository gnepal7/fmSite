# fm/models.py
from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone

class MediaFile(models.Model):
    """Reusable image / audio / document library."""
    file = models.FileField(upload_to='cabinet/library/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    alt_text = models.CharField(max_length=200, blank=True, help_text="Optional description")

    def __str__(self):
        return self.file.name.split('/')[-1]

    class Meta:
        ordering = ['-uploaded_at']

# 1. Home / Posts (Reusable Content Block)
class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='news_images')
    content = HTMLField()
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'News Post'
        verbose_name_plural = 'News Posts'

    def __str__(self):
        return self.title

# 2. Static Pages (About, Contact, etc.)
class Page(models.Model):
    PAGE_CHOICES = [
        ('about', 'About Us'),
        ('team', 'Our Team'),
        ('schedule', 'Program Schedule'),
        ('archive', 'Archive'),
        ('contact', 'Contact'),
    ]
    slug = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200, blank=True)
    image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='page_images')
    content = HTMLField(blank=True)

    def __str__(self):
        return dict(self.PAGE_CHOICES)[self.slug]

# 3. Team Members (Subcategory under 'Our Team')
class TeamMember(models.Model):
    CATEGORY_CHOICES = [
        ('executive', 'Executive Team'),
        ('staff', 'Staff'),
        ('board', 'Board Members'),
        ('shareholder', 'Share Holders'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    profile_image = models.ForeignKey(MediaFile, on_delete=models.PROTECT,
                                      related_name='team_images')

    def __str__(self):
        return f"{self.name} - {self.designation}"

# 4. Program Schedule (Daily, 7 days)
class ProgramSchedule(models.Model):
    DAYS = [(i, timezone.now().replace(day=i).strftime('%A')) for i in range(1, 8)]
    day = models.IntegerField(choices=DAYS)  # 1=Mon, ..., 7=Sun
    program_name = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('day', 'start_time', 'program_name')
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.program_name} ({self.get_day_display()})"

# 5. Archive Audio Programs
class ArchiveProgram(models.Model):
    program_name = models.CharField(max_length=200)
    broadcast_date = models.DateField(default=timezone.now)
    audio_file = models.ForeignKey(MediaFile, on_delete=models.PROTECT,
                                   related_name='archive_audio')
    featured_image = models.ForeignKey(MediaFile, on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='archive_images')

    class Meta:
        ordering = ['-broadcast_date']

    def __str__(self):
        return f"{self.program_name} - {self.broadcast_date}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Slider(models.Model):
    image = models.ForeignKey(MediaFile, on_delete=models.CASCADE,
                              related_name='slider_images')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.caption or f"Slide {self.id}"

class GalleryImage(models.Model):
    gallery = models.ForeignKey('Gallery', on_delete=models.CASCADE,
                                related_name='images')
    image = models.ForeignKey(MediaFile, on_delete=models.CASCADE,
                              related_name='gallery_images')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or self.image.file.name.split('/')[-1]

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SiteLogo(models.Model):
    logo = models.ForeignKey(MediaFile, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='site_logo')
    class Meta:
        verbose_name = "Site Logo"
        verbose_name_plural = "Site Logo"

    def __str__(self):
        return "Current Site Logo"