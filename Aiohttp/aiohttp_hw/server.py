from aiohttp import web

from routs import routs
from views import orm_context, session_middleware

app = web.Application()
app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

app.add_routes(routs)


if __name__ == '__main__':
    web.run_app(app)
