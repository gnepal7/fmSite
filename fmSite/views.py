from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from django.contrib import messages

from django.db.models import Max
from fm import models
from fm.forms import ContactForm
from fm.models import ArchiveProgram, Page, ProgramSchedule, Slider, NewsPost, Gallery, TeamMember

def homePage(request):
    sliders = Slider.objects.all().order_by('order', '-id')
    about = get_object_or_404(Page, slug='about')
    newsItems = NewsPost.objects.all().order_by('-id')[:6]
    # programs = ArchiveProgram.objects.all().order_by('-broadcast_date')[:3]
    # program = programs[0] if programs else None   
    latest_programs = ArchiveProgram.objects.values('program_name') \
        .annotate(latest_id=Max('id')) \
        .values_list('latest_id', flat=True)    
    programs = ArchiveProgram.objects.filter(id__in=latest_programs) \
        .order_by('-broadcast_date')[:3]
    program = programs[0] if programs else None


    galleries = Gallery.objects.all().prefetch_related('images')
    homeData = {
        'title' : 'FM site template',
        'sliderItems' : sliders,
        'aboutUs': about, 
        'news' : newsItems,
        'programs': programs,
        'galleries': galleries,
        'program': program
    }
    return render(request, 'index.html', homeData)

def aboutPage(request):
    about = get_object_or_404(Page, slug='about')  
    return render(request, 'page.html', {'page': about, 'title': 'About us'})

def newsDetail(request, id):
    post = get_object_or_404(NewsPost, id=id, is_published=True)
    return render(request, 'detail.html', {'post': post, 'title': post.title})
    
# pagination
def news_list(request):
    posts = NewsPost.objects.filter(is_published=True).order_by('-published_at')
    paginator = Paginator(posts, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'page_obj': page_obj, 'title': 'News Collection'})

def archievPage(request):    
    archievPrograms = ArchiveProgram.objects.values('program_name') \
        .annotate(latest_id=Max('id')) \
        .values_list('latest_id', flat=True)
    programs = ArchiveProgram.objects.filter(id__in=archievPrograms) \
        .order_by('-broadcast_date')
    # ap = archievPrograms[0] if archievPrograms else None  
    paginator = Paginator(programs, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'archiev.html', {'page_obj': page_obj, 'title': 'Program Archiev'})

def program_detail(request, id):
    program = get_object_or_404(ArchiveProgram, id=id)
    related = ArchiveProgram.objects.filter(
        program_name=program.program_name
    ).exclude(id=id).order_by('-broadcast_date')[:20]
    return render(request, 'archiev-detail.html', {
        'program': program,
        'related': related,
        'title' : 'Program List'
    })

def teamPage(request, category):
    category_map = {
        'executive' : 'executive',
        'staff' : 'staff',
        'board' : 'board',
        'shareholder': 'shareholder',
    }
    cat_key = category_map.get(category)
    if not cat_key:
        cat_key = 'board'
    
    members = TeamMember.objects.filter(category=cat_key)
    title = dict(TeamMember.CATEGORY_CHOICES).get(cat_key, 'Team')

    return render(request, 'team.html', {
        'members' : members,
        'title' : title,
        'category' : category
    })

def programSchedulePage(request):
    schedule = ProgramSchedule.objects.all().order_by('day', 'start_time')
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    return render(request, 'schedule.html', {
        'schedule': schedule,
        'days': days,
        'title' : 'Program Schedule'
    })


from django.contrib import messages  # ← ADD THIS

def contactPage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
                f"Contact from {form.cleaned_data['name']}",
                form.cleaned_data['message'],
                form.cleaned_data['email'],
                ['gnepal7@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'title' : 'Contact us'})