from flask import request, render_template

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapper.spiders.fintech import Fintech
from scrapper.spiders.currency import Currency
from multiprocessing import Process

from app import create_app


app = create_app()
app.app_context().push()


def run_spider(spider, category=None):
	crawler = CrawlerProcess(get_project_settings())
	crawler.crawl(spider, category)
	crawler.start()


@app.route('/', strict_slashes=False)
def index():
	return render_template('index.html')


@app.route('/fintech/update/', methods=['POST'], strict_slashes=False)
def update_fintech():
	lang = request.form.get('lang')
	max_page = request.form.get('max_page')
	category = [max_page, lang]

	run_process = Process(target=run_spider, args=(Fintech, category))
	run_process.start()
	run_process.join()
	return render_template('successfull.html')


@app.route('/update_currency/', strict_slashes=False)
def update_currency():
	run_process = Process(target=run_spider, args=(Currency, ))
	run_process.start()
	run_process.join()
	return render_template('successfull.html')


if __name__ == '__main__':
	app.run(debug=True)