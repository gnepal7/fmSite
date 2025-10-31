# fm/context_processors.py
from .models import SiteLogo

def site_logo(request):
    logo = SiteLogo.objects.first()
    return {'site_logo': logo}