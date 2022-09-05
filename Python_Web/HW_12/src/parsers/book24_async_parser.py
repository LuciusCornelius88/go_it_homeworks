import requests
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
from src.db import Book
from src.settings import config


url = config['sources']['book24']



async def get_data(session, page, request):

	page_url = f'{url}?PAGEN_1={page}'

	async with session.get(url=page_url) as response:
		response_text = await response.text()
		soup = BeautifulSoup(response_text, 'lxml')

		books = soup.find_all('div', class_='item_info')

		for b in books:
			try:
				link = str(b.find('div', class_='item-title').find('a').get('href'))
			except:
				link = 'N/A'
			try:
				title = b.find('div', class_='item-title').find('a').find('span').text.strip()
			except:
				title = 'N/A'
			try:
				author = b.find('div', class_='article_block').find('a').text.strip()
			except:
				author = 'N/A'
			try:
				avialability = b.find('div', class_='item-stock').find('span', class_='value').text.strip()
			except:
				avialability = 'N/A'
			try:
				price = int(b.find('div', class_='price discount').find('span', class_='price_value').text.strip().replace(' ', ''))
			except:
				price = 0
			try:
				special_price = int(b.find('div', class_='price').find('span', class_='price_value').text.strip().replace(' ', ''))
				if price == 0:
					price = special_price
					special_price = 0
			except:
				special_price = 0


			book = Book(link=link, title=title, author=author, 
						avialability=avialability, price=price, special_price=special_price)

			current_book = request.app['db_session'].query(Book).filter(Book.link == link).first()
			
			if current_book: 
				if str(current_book) == str(book) or ((link == 'N/A') or (title == 'N/A')):
					continue
				else:
					request.app['db_session'].delete(current_book)
					request.app['db_session'].commit()

			request.app['db_session'].add(book)
			request.app['db_session'].commit()


async def gather_data(request):

	async with aiohttp.ClientSession() as session:

		response = await session.get(url=url)
		soup = BeautifulSoup(await response.text(), 'lxml')
		pages_count = int(soup.find('div', class_='module-pagination').find_all('a', class_='dark_link')[-1].text)

		tasks = []

		# for page in range(1, pages_count + 1):
		for page in range(1, 2):
			task = asyncio.create_task(get_data(session, page, request))
			tasks.append(task)

		await asyncio.gather(*tasks)
