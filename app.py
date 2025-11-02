from flask import Flask
from flask_smorest import Api
from api.resources.services import blp as services_blp
from api.resources.bookings import blp as bookings_blp
import logging


def create_app():
    app = Flask(__name__)

    app.config['API_TITLE'] = 'Mini Orgzaar API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    # Basit hata loglaması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.logger.info('Mini Orgzaar API başlatıldı')

    api = Api(app)
    api.register_blueprint(services_blp)
    api.register_blueprint(bookings_blp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
