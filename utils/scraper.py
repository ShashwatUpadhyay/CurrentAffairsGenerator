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
    url = 'https://www.ndtv.com/latest?pfrom=home-ndtv_mainnavigation'
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
                'title': title_element,
                'description': description_element,
                'image': image_element,
                'url': external_link
            }

            if 'ndtv.com' in external_link:
                response = requests.get(external_link, headers=header)
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.find('div', {'class': 'Art-exp_wr'})
                data['content'] = content.text.strip() if content else 'No Content'

            News.objects.create(**data)
            print(f"[NEWS SAVED] {title_element[:20]}...")

        except Exception as e:
            print(f"Error processing article: {str(e)}")
    
    return articles

print(fetch_news())
