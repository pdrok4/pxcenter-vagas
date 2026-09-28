import json, re, os
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

BASE = "https://pxcenter.inhire.app"
FILTRO = re.compile(r"design|ux|ui\b", re.I)  # só vagas de design; use None p/ todas

# mantém a data em que cada vaga apareceu pela 1ª vez
antigas = {}
if os.path.exists("vagas.json"):
    with open("vagas.json", encoding="utf-8") as f:
        antigas = {v["link"]: v for v in json.load(f)}

encontradas = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"{BASE}/vagas", wait_until="networkidle")
    try:
        page.wait_for_selector('a[data-component-name="job-position-link"]', timeout=20000)
        for a in page.query_selector_all('a[data-component-name="job-position-link"]'):
            titulo = a.query_selector('div[data-sentry-element="JobPositionName"]').inner_text().strip()
            encontradas.append((titulo, BASE + a.get_attribute("href")))
    except PWTimeout:
        print("Nenhuma vaga listada (ou a página mudou)")
    browser.close()

agora = datetime.now(timezone.utc).isoformat()
vagas = []
for titulo, link in encontradas:
    if FILTRO and not FILTRO.search(titulo):
        continue
    vagas.append(antigas.get(link, {"titulo": titulo, "link": link, "data": agora}))

with open("vagas.json", "w", encoding="utf-8") as f:
    json.dump(vagas, f, indent=2, ensure_ascii=False)

print(f"Total no site: {len(encontradas)} | Design: {len(vagas)}")
