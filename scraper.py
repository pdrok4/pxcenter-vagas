import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

url = "https://pxcenter.inhire.app/vagas"

# Faz o scrape
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extrai as vagas (você vai precisar inspecionar a página pra saber os seletores exatos)
vagas = []
for vaga in soup.select('[class*="vaga"]'):  # ajusta o seletor conforme preciso
    titulo = vaga.select_one('h2, .title')
    link = vaga.select_one('a')
    if titulo and link:
        vagas.append({
            'titulo': titulo.text.strip(),
            'link': link.get('href'),
            'data': datetime.now().isoformat()
        })

# Salva em JSON
with open('vagas.json', 'w') as f:
    json.dump(vagas, f, indent=2)

print(f"Encontradas {len(vagas)} vagas")
