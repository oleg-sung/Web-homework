from sqlalchemy.exc import IntegrityError
from aiohttp import web

from errors import validate, get_http_errors
from models import Base, engine, Ad, Session
from schema import CreateAd, UpdateAd


async def orm_context(app: web.Application):
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request['session'] = session
        response = await handler(request)
        return response


class AdView(web.View):
    @property
    def session(self) -> Session:
        return self.request['session']

    @property
    def get_ad_id(self) -> int:
        return int(self.request.match_info['ad_id'])

    @staticmethod
    async def get_ad(ad_id: int, session: Session) -> Ad:
        ad = await session.get(Ad, ad_id)
        if ad is None:
            raise get_http_errors(web.HTTPNotFound, 'user not found')
        return ad

    async def get(self):
        ad = await self.get_ad(self.get_ad_id, self.session)
        return web.json_response({
            'owner': ad.owner,
            'title': ad.title,
            'text': ad.text,
            'creation_time': ad.create_ad.isoformat()
        })

    async def post(self):
        json_data = validate(await self.request.json(), CreateAd)
        new_ad = Ad(**json_data)
        try:
            self.session.add(new_ad)
            await self.session.commit()
        except IntegrityError:
            raise get_http_errors(web.HTTPConflict, 'user already exists')
        return web.json_response({
            'id': new_ad.id,
        })

    async def patch(self):
        json_data = validate(await self.request.json(), UpdateAd)
        ad = await self.get_ad(self.get_ad_id, self.session)
        if not json_data:
            raise get_http_errors(web.HTTPBadRequest, 'key error')
        for key, value in json_data.items():
            setattr(ad, key, value)
        try:
            self.session.add(ad)
            await self.session.commit()
        except IntegrityError:
            raise get_http_errors(web.HTTPConflict, 'user already exists')
        return web.json_response({'status': "OK",
                                  'id': ad.id
                                  })

    async def delete(self):
        ad = await self.get_ad(self.get_ad_id, self.session)
        await self.session.delete(ad)
        await self.session.commit()
        return web.json_response({'status': 'deleted'})
