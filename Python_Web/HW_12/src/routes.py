from aiohttp.web import Application
from src.views import index, successful, update, get_avialable, sort_by_price, special_price


def setup_routes(app: Application):
    app.router.add_get('/', index)
    app.router.add_get('/successful/', successful, name='successful')
    app.router.add_get('/update/', update, name='update')
    app.router.add_get('/get_avialable/', get_avialable, name='get_avialable')
    app.router.add_get('/sort_by_price/', sort_by_price, name='sort_by_price')
    app.router.add_get('/special_price/', special_price, name='special_price')
		