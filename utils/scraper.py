import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ca_gen.settings')
django.setup()

import requests
from bs4 import BeautifulSoup
from base.models import News
from utils.translator import translate_to_hindi, translate_to_english

def test_url():
    url = 'https://www.ndtv.com/india-news/cash-payments-to-be-banned-at-toll-plazas-from-april-1-heres-the-big-update-10763805'
    header = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', {'class': 'Art-exp_wr'})
    print(content.text.strip())

def fetch_news():
    url = 'https://ndtv.in/latest-news?pfrom=home-khabar_nav'
    header = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    news = soup.find_all('li', {'class': 'NwsLstPg-a-li'})
    for article in news:
        try:
            title_element = article.find('a', {'class': 'NwsLstPg_ttl-lnk'})
            description_element = article.find('p', {'class': 'NwsLstPg_txt txt_tct txt_tct-three'})
            external_link = title_element['href'] if title_element is not None else ''  
            image_element = article.find('img', {'class': 'NwsLstPg_img-full'})


            title_element = title_element.text.strip() if title_element else 'No Title'
            description_element = description_element.text.strip() if description_element else 'No Description'
            image_element = image_element['src'] if image_element is not None else ''

            data = {
                'title': translate_to_english(title_element),
                'title_hi': translate_to_hindi(title_element),
                'description': translate_to_english(description_element),
                'description_hi': translate_to_hindi(description_element),
                'image': image_element,
                'url': external_link
            }

            if 'ndtv.in' in external_link:
                response = requests.get(external_link, headers=header)
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find('div', {'class': 'Art-exp_wr'})
                data['content'] = translate_to_english(content.text.strip()) if content else 'No Content'
                data['content_hi'] = translate_to_hindi(content.text.strip()) if content else 'No Content'

            News.objects.create(**data)
            print(f"\n [NEWS SAVED] \n {data}...")

        except Exception as e:
            print(f"Error processing article: {str(e)}")
    
    return articles

print(fetch_news())
