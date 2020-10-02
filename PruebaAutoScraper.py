from autoscraper import AutoScraper

url = 'https://www.rosario3.com/'

wanted_list = ["/especiales/Club-de-Lectura-Brandon-Sanderson-es-mejor-que-J.-R.-R.-Tolkien-20200909-0043.html"]

scraper = AutoScraper()
result = scraper.build(url, wanted_list)

dict = scraper.get_result_exact(url, unique=False,grouped=True)
l=[]
[l.extend([k,v]) for k,v in dict.items()]

regla = l[0]
scraper.set_rule_aliases({regla: 'regla'})

scraper.keep_rules([regla])

scraper.save('rosario3-search')