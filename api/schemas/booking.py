from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BookingRequestSchema(Schema):
    service_ids = fields.List(fields.Int(), required=True, error_messages={
        'required': 'service_ids alanı zorunludur.',
        'type': 'service_ids bir liste olmalıdır.'
    })
    event_date = fields.Str(required=True, error_messages={
        'required': 'event_date alanı zorunludur.'
    })
    notes = fields.Str(required=False, allow_none=True)

    @validates('event_date')
    def validate_event_date(self, value):
        """Tarih formatını ve gelecekte olup olmadığını kontrol et"""
        if not value:
            logger.error('Boş tarih girildi')
            raise ValidationError('event_date alanı boş olamaz.')

        try:
            date_obj = datetime.strptime(value, '%Y-%m-%d')
            if date_obj.date() < datetime.now().date():
                logger.warning(f'Geçmiş tarih girildi: {value}')
                raise ValidationError('Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır.')
        except ValueError as e:
            logger.error(f'Geçersiz tarih formatı: {value}')
            raise ValidationError('Tarih formatı YYYY-MM-DD olmalıdır ve gelecek bir tarih olmalıdır.')

    @validates_schema
    def validate_schema(self, data, **kwargs):
        """Genel şema validasyonu"""
        # service_ids listesinin içindeki değerleri kontrol et
        if 'service_ids' in data and data['service_ids']:
            for service_id in data['service_ids']:
                if not isinstance(service_id, int) or service_id <= 0:
                    logger.error(f'Geçersiz service_id: {service_id}')
                    raise ValidationError('service_ids listesindeki değerler pozitif tam sayı olmalıdır.', 'service_ids')


class BookingResponseSchema(Schema):
    message = fields.Str(required=True)
    booking_id = fields.Int(required=True)
