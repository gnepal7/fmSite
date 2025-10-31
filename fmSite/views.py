from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from fm.models import Page, Slider, NewsPost

def homePage(request):
    sliders = Slider.objects.all().order_by('order', '-id')
    about = get_object_or_404(Page, slug='about')
    newsItems = NewsPost.objects.all().order_by('-id')[:6]
    homeData = {
        'sliderItems' : sliders,
        'aboutUs': about, 
        'news' : newsItems
    }
    return render(request, 'index.html', homeData)

def aboutPage(request):
    about = get_object_or_404(Page, slug='about')  
    return render(request, 'page.html', {'page': about})

def newsPage(request):
    newsList = NewsPost.objects.all().order_by('-id') 
    return render(request, 'news.html', {'newsList': newsList})

def newsDetail(request, id):
    post = get_object_or_404(NewsPost, id=id, is_published=True)
    return render(request, 'detail.html', {'post': post})
    

# pagination
def news_list(request):
    posts = NewsPost.objects.filter(is_published=True).order_by('-published_at')
    paginator = Paginator(posts, 1)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news_list.html', {'page_obj': page_obj})