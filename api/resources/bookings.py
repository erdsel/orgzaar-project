from flask.views import MethodView
from flask_smorest import Blueprint
from api.schemas.booking import BookingRequestSchema, BookingResponseSchema
import random
import logging

logger = logging.getLogger(__name__)

blp = Blueprint('bookings', __name__, url_prefix='/api/v1', description='Rezervasyon İşlemleri')


@blp.route('/bookings')
class Bookings(MethodView):

    @blp.arguments(BookingRequestSchema)
    @blp.response(201, BookingResponseSchema)
    def post(self, booking_data):
        logger.info(f'Rezervasyon talebi alındı: {booking_data}')
        booking_id = random.randint(1000, 9999)
        logger.info(f'Rezervasyon oluşturuldu. ID: {booking_id}')
        return {"message": "Rezervasyon talebiniz alındı.", "booking_id": booking_id}
