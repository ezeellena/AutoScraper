import json

from autoscraper import AutoScraper
from flask import Flask, request,render_template


PAGINA_scraper = AutoScraper()
PAGINA_scraper.load('./rosario3-search')
app = Flask(__name__)

def get_pagina_result(url,link):
    PAGINA_scraper = AutoScraper()
    PAGINA_scraper.load('./'+url+'-search')
    result = PAGINA_scraper.get_result_similar(link, group_by_alias=True)
    return _aggregate_result(result)


def _aggregate_result(result):
    final_result = []
    for i in range(len(list(result.values())[0])):
        final_result.append({alias: result[alias][i] for alias in result})
    return final_result


@app.route('/AutoScraper', methods=['GET'])
def autoscraper(Link=None,Metodo=None):
    url = request.args["Link"]
    link = request.args["Link"]
    Metodo = request.args["Metodo"]
    wanted_list = [Metodo]
    scraper = AutoScraper()
    scraper.build(link, wanted_list)
    dict = scraper.get_result_exact(link, unique=False, grouped=True)
    l = []
    [l.extend([k, v]) for k, v in dict.items()]
    regla = l[0]
    scraper.set_rule_aliases({regla: 'regla'})
    scraper.keep_rules([regla])
    url = url.replace("http:", "").replace("//", "").replace(".", "").replace("www", "").replace(
        "https:", "").replace("/", "").replace("\n", "").replace("-", "")
    scraper.save(url+'-search')
    data = get_pagina_result(url,link)
    json_format = json.dumps(data, indent=4, separators=(',', ': '), sort_keys=True,ensure_ascii=False)
    return json_format

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/rosario3', methods=['GET'])
def search_api():
    return dict(result=get_pagina_result())


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')