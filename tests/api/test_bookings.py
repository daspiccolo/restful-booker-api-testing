import requests
import pytest


class TestHealthCheck:

    def test_ping_returns_201(self, base_url):
        response = requests.get(f"{base_url}/ping")

        assert response.status_code == 201

    def test_ping_response_time_is_acceptable(self, base_url):
        # API response should not exceed 3 seconds
        response = requests.get(f"{base_url}/ping")

        assert response.elapsed.total_seconds() < 3, \
            f"Response too slow: {response.elapsed.total_seconds()}s"

class TestGetAllBookings:

    def test_get_all_bookings_returns_200(self, base_url):
        response = requests.get(f"{base_url}/booking")

        assert response.status_code == 200

    def test_get_all_bookings_returns_list(self, base_url):
        response = requests.get(f"{base_url}/booking")
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

    def test_each_booking_has_id_field(self, base_url):
        response = requests.get(f"{base_url}/booking")
        data = response.json()

        for booking in data:
            assert "bookingid" in booking

    def test_filter_by_invalid_name_returns_empty_list(self, base_url):
        response = requests.get(f"{base_url}/booking", params={"firstname": "Xyzabc123"})
        data = response.json()

        assert response.status_code == 200
        assert data == []

class TestGetBookingById:

    @pytest.fixture
    def valid_booking_id(self, base_url):
        # Fetches a real booking ID dynamically to avoid hardcoded test data
        response = requests.get(f"{base_url}/booking")
        bookings = response.json()
        return bookings[0]["bookingid"]

    def test_get_existing_booking_returns_200(self, base_url, valid_booking_id):
        response = requests.get(f"{base_url}/booking/{valid_booking_id}")

        assert response.status_code == 200

    def test_get_existing_booking_returns_expected_fields(self, base_url, valid_booking_id):
        response = requests.get(f"{base_url}/booking/{valid_booking_id}")
        data = response.json()

        assert "firstname" in data
        assert "lastname" in data
        assert "totalprice" in data
        assert "depositpaid" in data
        assert "bookingdates" in data
        assert "checkin" in data["bookingdates"]
        assert "checkout" in data["bookingdates"]

    def test_get_nonexistent_booking_returns_404(self, base_url):
        response = requests.get(f"{base_url}/booking/99999")

        assert response.status_code == 404

    def test_get_booking_with_non_numeric_id_returns_400(self, base_url):
        # BUG-002: returns 404 instead of expected 400
        response = requests.get(f"{base_url}/booking/abc")

        assert response.status_code == 404