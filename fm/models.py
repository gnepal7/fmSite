# fm/models.py
from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone

# 1. Home / Posts (Reusable Content Block)
class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='cabinet/news/', blank=True, null=True)
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
    image = models.ImageField(upload_to='cabinet/pages/', blank=True)
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
    profile_image = models.ImageField(upload_to='cabinet/team/')

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
    audio_file = models.FileField(upload_to='cabinet/audio/')
    featured_image = models.ImageField(upload_to='cabinet/archive/', blank=True)

    class Meta:
        ordering = ['-broadcast_date']

    def __str__(self):
        return f"{self.program_name} - {self.broadcast_date}"

# 6. Contact Form Submission
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"