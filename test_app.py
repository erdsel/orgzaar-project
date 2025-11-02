import pytest
from app import create_app
from datetime import datetime, timedelta


@pytest.fixture
def app():
    """Flask uygulamasını test için oluştur"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Test client oluştur"""
    return app.test_client()


class TestServicesEndpoint:
    """Hizmetler endpoint'i için testler"""

    def test_get_services_success(self, client):
        """GET /api/v1/services başarılı yanıt testi"""
        response = client.get('/api/v1/services')

        assert response.status_code == 200
        data = response.get_json()

        assert isinstance(data, list)
        assert len(data) == 3

        # İlk hizmeti kontrol et
        first_service = data[0]
        assert first_service['id'] == 1
        assert first_service['name'] == "DJ Hizmeti (2 Saat)"
        assert first_service['category'] == "Müzik & Sanatçı"
        assert first_service['price'] == 5000

    def test_get_services_returns_all_fields(self, client):
        """Tüm hizmetlerin gerekli alanları içerdiğini test et"""
        response = client.get('/api/v1/services')
        data = response.get_json()

        for service in data:
            assert 'id' in service
            assert 'name' in service
            assert 'category' in service
            assert 'price' in service


class TestBookingsEndpoint:
    """Rezervasyon endpoint'i için testler"""

    def test_post_booking_success(self, client):
        """Başarılı rezervasyon talebi testi"""
        future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        booking_data = {
            "service_ids": [1, 3],
            "event_date": future_date,
            "notes": "Test rezervasyonu"
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 201
        data = response.get_json()

        assert data['message'] == "Rezervasyon talebiniz alındı."
        assert 'booking_id' in data
        assert 1000 <= data['booking_id'] <= 9999

    def test_post_booking_without_notes(self, client):
        """Notes olmadan rezervasyon testi"""
        future_date = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')

        booking_data = {
            "service_ids": [2],
            "event_date": future_date
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 201
        data = response.get_json()
        assert 'booking_id' in data

    def test_post_booking_empty_service_ids(self, client):
        """Boş service_ids listesi testi"""
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')

        booking_data = {
            "service_ids": [],
            "event_date": future_date,
            "notes": "Test"
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 201

    def test_post_booking_missing_service_ids(self, client):
        """service_ids alanı eksik testi"""
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')

        booking_data = {
            "event_date": future_date,
            "notes": "Test"
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 422

    def test_post_booking_missing_event_date(self, client):
        """event_date alanı eksik testi"""
        booking_data = {
            "service_ids": [1],
            "notes": "Test"
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 422

    def test_post_booking_invalid_date_format(self, client):
        """Geçersiz tarih formatı testi"""
        booking_data = {
            "service_ids": [1],
            "event_date": "24-12-2025",  # Yanlış format
            "notes": "Test"
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 422
        data = response.get_json()
        assert 'errors' in data

    def test_post_booking_past_date(self, client):
        """Geçmiş tarih testi"""
        past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        booking_data = {
            "service_ids": [1],
            "event_date": past_date,
            "notes": "Test"
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 422
        data = response.get_json()
        assert 'errors' in data

    def test_post_booking_invalid_service_ids_type(self, client):
        """service_ids tipi geçersiz testi"""
        future_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')

        booking_data = {
            "service_ids": "not-a-list",
            "event_date": future_date
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        assert response.status_code == 422

    def test_post_booking_today_date(self, client):
        """Bugünün tarihi testi (gelecek sayılır, başarılı olmalı)"""
        today = datetime.now().strftime('%Y-%m-%d')

        booking_data = {
            "service_ids": [1],
            "event_date": today
        }

        response = client.post('/api/v1/bookings',
                              json=booking_data,
                              content_type='application/json')

        # Bugün geçmiş sayılmaz, başarılı olmalı
        assert response.status_code == 201
        data = response.get_json()
        assert 'booking_id' in data


class TestAPIBasics:
    """Genel API testleri"""

    def test_app_exists(self, app):
        """Uygulama oluşturulabilir mi?"""
        assert app is not None

    def test_app_is_testing(self, app):
        """Uygulama test modunda mı?"""
        assert app.config['TESTING'] is True

    def test_invalid_endpoint(self, client):
        """Var olmayan endpoint testi"""
        response = client.get('/api/v1/invalid')
        assert response.status_code == 404
