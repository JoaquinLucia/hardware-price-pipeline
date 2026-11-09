from app.servicios.crawler import CrawlerCategorias

print("--- PROBANDO CRAWLER DE VENEX ---")
url_venex = "https://www.venex.com.ar/componentes-de-pc/microprocesadores"
links_v = CrawlerCategorias.extraer_links(url_venex)
print(f"Se encontraron {len(links_v)} procesadores en Venex.")
if links_v:
    print(f"Primer link: {links_v[0]}\n")

print("--- PROBANDO CRAWLER DE FULLH4RD ---")
url_full = "https://www.fullh4rd.com.ar/cat/search/microprocesador"
links_f = CrawlerCategorias.extraer_links(url_full)
print(f"Se encontraron {len(links_f)} procesadores en FullH4rd.")
if links_f:
    print(f"Primer link: {links_f[0]}")