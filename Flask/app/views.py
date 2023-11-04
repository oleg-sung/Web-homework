from flask import jsonify
from flask.views import MethodView
from flask import request

from errors import HttpError, validate
from models import Ad, Session
from schema import CreateAd, UpdateAd


def get_ad(ad_id: int, session: Session):
    ad = session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, 'ad not found')
    return ad


class AdsView(MethodView):
    def get(self, ads_id):
        with Session() as session:
            ad = get_ad(ads_id, session)
            return jsonify({
                'title': ad.title,
                'text': ad.text,
                'owner': ad.owner,
                'create_ad': ad.create_ad
            })

    def post(self):
        json_data = validate(request.json, CreateAd)
        with Session() as session:
            new_ad = Ad(**json_data)
            if session.query(Ad).filter(Ad.title == new_ad.title, Ad.owner == new_ad.owner,
                                        Ad.text == new_ad.text) is not None:
                raise HttpError(418, 'ad already exists')
            session.add(new_ad)
            session.commit()
            return jsonify({
                'id': new_ad.id,
                'title': new_ad.title,
                'create_ad': new_ad.create_ad
            })

    def patch(self, ads_id):
        json_data = validate(request.json, UpdateAd)
        with Session() as session:
            ad = get_ad(ads_id, session)
            for key, value in json_data.items():
                setattr(ad, key, value)
            session.add(ad)
            session.commit()
            return jsonify({
                'status': 'success'
            })

    def delete(self, ads_id):
        with Session() as session:
            ad = get_ad(ads_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({
                'status': 'success'
            })
