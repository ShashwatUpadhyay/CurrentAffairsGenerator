import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ca_gen.settings')
django.setup()

from utils.scraper import fetch_news
from utils.translator import translate_to_hindi
from utils.mcq_generator import generate_mcqs
from base.models import News

def master():
    fetch_news()
    print("[NEWS SCRAPED] All news scraped.")
    return True