import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://sg.search.yahoo.com/search'

def search_internet(query, num_results=4):
    params = {
        'q': query,
        'btf': 'w',
        'nojs': '1',
        'ei': 'UTF-8',
        'vc': 'in',
    }
    response = requests.get(BASE_URL, params=params)

    if not response.ok:
        raise Exception(f"Failed to fetch: {response.status_code} {response.reason}")

    return html_to_search_results(response.text, num_results)

def extract_real_url(url):
    match = re.search(r'RU=([^/]+)', url)
    if match and match.group(1):
        return urllib.parse.unquote(match.group(1))

    return url

def html_to_search_results(html, num_results):
    results = []
    soup = BeautifulSoup(html, 'html.parser')

    right_panel = soup.select_one('#right .searchRightTop')
    if right_panel:
        right_panel_link = right_panel.select_one('.compText a')
        right_panel_info = right_panel.select('.compInfo li')
        right_panel_info_text = '\n'.join([el.get_text(strip=True) for el in right_panel_info])

        results.append({
            'title': right_panel_link.get_text(strip=True) if right_panel_link else '',
            'body': f"{right_panel.select_one('.compText').get_text(strip=True)}{f'{right_panel_info_text}' if right_panel_info_text else ''}",
            'url': extract_real_url(right_panel_link['href']) if right_panel_link else ''
        })

    for element in soup.select('.algo-sr:not([class*="ad"])')[:num_results]:
        title_element = element.select_one('h3.title a')
        description_element = element.select_one('.compText p')  # Extract text from 'p' element for description

        body_text = ''
        if description_element:
            body_text = description_element.get_text(strip=True)

        results.append({
            'title': title_element['aria-label'] if title_element else '',
            'body': body_text,
            'url': extract_real_url(title_element['href']) if title_element else ''
        })
    # Format search_results as a string to be understood by your AI
    formatted_results = "\n".join([f"Title- {result['title']}\nBody- {result['body']}\nURL- {result['url']}\n" for result in results])
    return formatted_results