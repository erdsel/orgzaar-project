from flask.views import MethodView
from flask_smorest import Blueprint
from api.schemas.service import ServiceSchema
import logging

logger = logging.getLogger(__name__)

blp = Blueprint('services', __name__, url_prefix='/api/v1', description='Hizmet İşlemleri')


SERVICES = [
    {"id": 1, "name": "DJ Hizmeti (2 Saat)", "category": "Müzik & Sanatçı", "price": 5000},
    {"id": 2, "name": "Masa Süsleme (Romantik)", "category": "Dekorasyon & Süsleme", "price": 1500},
    {"id": 3, "name": "Catering (Kişi Başı)", "category": "Yemek & İkram", "price": 800}
]


@blp.route('/services')
class Services(MethodView):

    @blp.response(200, ServiceSchema(many=True))
    def get(self):
        logger.info('Hizmet listesi istendi')
        return SERVICES
