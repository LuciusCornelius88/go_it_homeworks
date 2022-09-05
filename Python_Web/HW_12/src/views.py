import asyncio
import aiohttp
import aiohttp_jinja2
from sqlalchemy import desc, func
from src.db import Book
from src.parsers import yakaboo_async_parser, book24_async_parser


@aiohttp_jinja2.template('index.html')
def index(request):
    return {}


@aiohttp_jinja2.template('output.html')
def get_avialable(request):
    books = request.app['db_session'].query(Book).filter(Book.avialability != 'N/A').all()
    return {'books': books}


@aiohttp_jinja2.template('output.html')
def sort_by_price(request):
    books = request.app['db_session'].query(Book).order_by(desc(Book.price)).all()
    return {'books': books}


@aiohttp_jinja2.template('output.html')
def special_price(request):
    books = request.app['db_session'].query(Book).filter(Book.special_price != 0).all()
    return {'books': books}


@aiohttp_jinja2.template('successful.html')
def successful(request):
    return {}


async def parse_resources(request):

    yakaboo = asyncio.create_task(yakaboo_async_parser.gather_data(request))
    book24 = asyncio.create_task(book24_async_parser.gather_data(request))

    await asyncio.gather(book24, yakaboo)

    
async def update(request):
    await parse_resources(request)

    return aiohttp.web.HTTPFound(location=request.app.router['successful'].url_for())


