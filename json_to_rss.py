from feedgen.feed import FeedGenerator
import json

fg = FeedGenerator()
fg.id('https://pxcenter-vagas.github.io')
fg.title('PX Center - Novas Vagas')
fg.link(href='https://pxcenter.inhire.app/vagas', rel='alternate')
fg.description('Monitoramento de vagas de designer na PX Center')

with open('vagas.json', 'r') as f:
    vagas = json.load(f)

for vaga in vagas:
    fe = fg.add_entry()
    fe.id(vaga['link'])
    fe.title(vaga['titulo'])
    fe.link(href=vaga['link'])
    fe.description(f"Publicada em {vaga['data']}")

fg.rss_file('feed.xml')
print("RSS gerado com sucesso!")
