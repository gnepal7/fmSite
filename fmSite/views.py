from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from django.db.models import Max
from fm import models
from fm.models import ArchiveProgram, Page, ProgramSchedule, Slider, NewsPost, Gallery, TeamMember

def homePage(request):
    sliders = Slider.objects.all().order_by('order', '-id')
    about = get_object_or_404(Page, slug='about')
    newsItems = NewsPost.objects.all().order_by('-id')[:6]
    programs = ArchiveProgram.objects.all().order_by('-broadcast_date')[:3]
    program = programs[0] if programs else None   
    galleries = Gallery.objects.all().prefetch_related('images')
    homeData = {
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
    return render(request, 'page.html', {'page': about})

def newsDetail(request, id):
    post = get_object_or_404(NewsPost, id=id, is_published=True)
    return render(request, 'detail.html', {'post': post})
    
# pagination
def news_list(request):
    posts = NewsPost.objects.filter(is_published=True).order_by('-published_at')
    paginator = Paginator(posts, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news.html', {'page_obj': page_obj})

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
    return render(request, 'archiev.html', {'page_obj': page_obj})

def program_detail(request, id):
    program = get_object_or_404(ArchiveProgram, id=id)
    related = ArchiveProgram.objects.filter(
        program_name=program.program_name
    ).exclude(id=id).order_by('-broadcast_date')[:20]
    return render(request, 'archiev-detail.html', {
        'program': program,
        'related': related
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
        'days': days
    })