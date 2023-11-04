from aiohttp import web

from views import AdView

routs = [
        web.get('/api/v1/ad/{ad_id:\d+}/', AdView),
        web.patch('/api/v1/ad/{ad_id:\d+}/', AdView),
        web.delete('/api/v1/ad/{ad_id:\d+}/', AdView),
        web.post('/api/v1/ad/', AdView)
]
