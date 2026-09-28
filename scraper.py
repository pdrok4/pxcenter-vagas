import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://pxcenter.inhire.app/vagas"

# Faz o scrape
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extrai as vagas
vagas = []
for vaga_li in soup.select('li[data-sentry-element="JobPositionLi"]'):
    titulo_elem = vaga_li.select_one('div[data-sentry-element="JobPositionName"]')
    link_elem = vaga_li.select_one('a[data-component-name="job-position-link"]')
    
    if titulo_elem and link_elem:
        titulo = titulo_elem.text.strip()
        href = link_elem.get('href', '')
        link_completo = f"https://pxcenter.inhire.app{href}" if href.startswith('/') else href
        
        vagas.append({
            'titulo': titulo,
            'link': link_completo,
            'data': datetime.now().isoformat()
        })

# Salva em JSON
with open('vagas.json', 'w') as f:
    json.dump(vagas, f, indent=2, ensure_ascii=False)

print(f"✅ Encontradas {len(vagas)} vagas")
