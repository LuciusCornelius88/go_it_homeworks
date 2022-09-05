import requests
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup
from src.db import Book
from src.settings import config


url = config['sources']['yakaboo']


async def get_data(session, page, request):

	page_url = f'{url}&p={page}'

	async with session.get(url=page_url) as response:
		response_text = await response.text()
		soup = BeautifulSoup(response_text, 'lxml')

		books = soup.find_all('div', class_='caption')

		for b in books:

			try:
				link = str(b.find('a').get('href'))
			except:
				link = 'N/A'
			try:
				title = b.find('div', class_='name').text.strip()
			except:
				title = 'N/A'
			try:
				author = b.find('div', class_='product-author').text.strip()
			except:
				author = 'N/A'
			try:
				avialability = b.find('div', class_='day_delivery').text.strip()
			except:
				avialability = 'N/A'
			try:
				price = b.find('div', class_='price-box').find('p', class_='old-price').find('span', class_='price').text
				price = int(price.strip().split(' ')[0].replace(' ', ''))
			except:
				try:
					price = b.find('div', class_='price-box').find('span', class_='regular-price').find('span', class_='price').text
					price = int(price.strip().split(' ')[0].replace(' ', ''))
				except:
					price = 0 
			try:
				special_price = b.find('div', class_='price-box').find('p', class_='special-price').find('span', class_='price').text
				special_price = int(special_price.strip().split(' ')[0].replace(' ', ''))
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
		pages_count = int(soup.find('div', class_='pagination').find('a', class_='last').text)

		tasks = []

		# for page in range(1, pages_count + 1):
		for page in range(1, 2):
			task = asyncio.create_task(get_data(session, page, request))
			tasks.append(task)

		await asyncio.gather(*tasks)