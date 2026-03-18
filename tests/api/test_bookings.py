import requests
import pytest

from conftest import base_url


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

class TestAuth:

    def test_valid_credentials_returns_token(self, base_url):
        payload = {
            "username": "admin",
            "password": "password123"
        }

        response = requests.post(f"{base_url}/auth", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert "token" in data
        assert len(data["token"]) > 0

    def test_invalid_credentials_returns_200_with_error(self, base_url):
        # BUG-003: API returns 200 instead of 401 for invalid credentials
        payload = {
            "username": "admin",
            "password": "wrongpassword"
        }

        response = requests.post(f"{base_url}/auth", json=payload)
        data = response.json()

        assert response.status_code == 200
        assert "reason" in data
        assert data["reason"] == "Bad credentials"

    def test_empty_credentials_returns_200_with_error(self, base_url):
        # BUG-003: API returns 200 instead of 400 for empty credentials
        payload = {
            "username": "",
            "password": ""
        }

        response = requests.post(f"{base_url}/auth", json=payload)

        assert response.status_code == 200

class TestCreateBooking:

    @pytest.fixture
    def booking_payload(self):
        return {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-06-01",
                "checkout": "2025-06-07"
            },
            "additionalneeds": "Breakfast"
        }

    def test_create_booking_returns_200(self, base_url, booking_payload):
        response = requests.post(f"{base_url}/booking", json=booking_payload)

        assert response.status_code == 200

    def test_create_booking_returns_booking_id(self, base_url, booking_payload):
        response = requests.post(f"{base_url}/booking", json=booking_payload)
        data = response.json()

        assert "bookingid" in data
        assert isinstance(data["bookingid"], int)

    def test_create_booking_returns_correct_data(self, base_url, booking_payload):
        response = requests.post(f"{base_url}/booking", json=booking_payload)
        data = response.json()["booking"]

        assert data["firstname"] == booking_payload["firstname"]
        assert data["lastname"] == booking_payload["lastname"]
        assert data["totalprice"] == booking_payload["totalprice"]
        assert data["depositpaid"] == booking_payload["depositpaid"]

    def test_create_booking_without_required_fields_returns_500(self, base_url):
    # BUG-004: API returns 500 instead of 400 for missing required fields
        payload = {"firstname": "Test"}

        response = requests.post(f"{base_url}/booking", json=payload)
        assert response.status_code == 500

class TestUpdateBooking:

    @pytest.fixture
    def created_booking(self, base_url, auth_token):
        # Creates a booking before each test and deletes it after
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-06-01",
                "checkout": "2025-06-07"
            },
            "additionalneeds": "Breakfast"
        }
        response = requests.post(f"{base_url}/booking", json=payload)
        booking_id = response.json()["bookingid"]

        yield booking_id

        # Cleanup — deletes the booking after the test finishes
        requests.delete(
            f"{base_url}/booking/{booking_id}",
            headers={"Cookie": f"token={auth_token}"}
        )

    def test_update_booking_returns_200(self, base_url, auth_token, created_booking):
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2025-07-01",
                "checkout": "2025-07-07"
            },
            "additionalneeds": "Lunch"
        }

        response = requests.put(
            f"{base_url}/booking/{created_booking}",
            json=payload,
            headers={"Cookie": f"token={auth_token}"}
        )

        assert response.status_code == 200

    def test_update_booking_returns_updated_data(self, base_url, auth_token, created_booking):
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2025-07-01",
                "checkout": "2025-07-07"
            },
            "additionalneeds": "Lunch"
        }

        response = requests.put(
            f"{base_url}/booking/{created_booking}",
            json=payload,
            headers={"Cookie": f"token={auth_token}"}
        )
        data = response.json()

        assert data["totalprice"] == 200
        assert data["additionalneeds"] == "Lunch"

    def test_update_booking_without_auth_returns_403(self, base_url, created_booking):
      
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2025-07-01",
                "checkout": "2025-07-07"
            },
            "additionalneeds": "Lunch"
        }

        response = requests.put(
            f"{base_url}/booking/{created_booking}",
            json=payload
        )

        assert response.status_code == 403

    def test_update_nonexistent_booking_returns_404(self, base_url, auth_token):
        # BUG-007: returns 405 instead of 404 for nonexistent booking
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2025-07-01",
                "checkout": "2025-07-07"
            },
            "additionalneeds": "Lunch"
        }

        response = requests.put(
            f"{base_url}/booking/99999",
            json=payload,
            headers={"Cookie": f"token={auth_token}"}
        )

        assert response.status_code == 405

class TestPartialUpdateBooking:

    @pytest.fixture
    def created_booking(self, base_url, auth_token):
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-06-01",
                "checkout": "2025-06-07"
            },
            "additionalneeds": "Breakfast"
        }
        response = requests.post(f"{base_url}/booking", json=payload)
        booking_id = response.json()["bookingid"]

        yield booking_id

        requests.delete(
            f"{base_url}/booking/{booking_id}",
            headers={"Cookie": f"token={auth_token}"}
        )

    def test_partial_update_returns_200(self, base_url, auth_token, created_booking):
        payload = {"totalprice": 300}

        response = requests.patch(
            f"{base_url}/booking/{created_booking}",
            json=payload,
            headers={"Cookie": f"token={auth_token}"}
        )

        assert response.status_code == 200

    def test_partial_update_changes_only_sent_fields(self, base_url, auth_token, created_booking):
        payload = {"totalprice": 300}

        response = requests.patch(
            f"{base_url}/booking/{created_booking}",
            json=payload,
            headers={"Cookie": f"token={auth_token}"}
        )
        data = response.json()

        assert data["totalprice"] == 300
        assert data["firstname"] == "Test"

    def test_partial_update_without_auth_returns_403(self, base_url, created_booking):
        payload = {"totalprice": 300}

        response = requests.patch(
            f"{base_url}/booking/{created_booking}",
            json=payload
        )

        assert response.status_code == 403

    def test_partial_update_with_empty_body_returns_200(self, base_url, auth_token, created_booking):
        # BUG-009: API accepts empty body without error
        response = requests.patch(
            f"{base_url}/booking/{created_booking}",
            json={},
            headers={"Cookie": f"token={auth_token}"}
        )

        assert response.status_code == 200


class TestDeleteBooking:

    @pytest.fixture
    def created_booking(self, base_url, auth_token):
        payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2025-06-01",
                "checkout": "2025-06-07"
            },
            "additionalneeds": "Breakfast"
        }
        response = requests.post(f"{base_url}/booking", json=payload)
        return response.json()["bookingid"]

    def test_delete_booking_returns_201(self, base_url, auth_token, created_booking):
        response = requests.delete(
            f"{base_url}/booking/{created_booking}",
            headers={"Cookie": f"token={auth_token}"}
        )

        assert response.status_code == 201

    def test_delete_booking_removes_resource(self, base_url, auth_token, created_booking):
        requests.delete(
            f"{base_url}/booking/{created_booking}",
            headers={"Cookie": f"token={auth_token}"}
        )

        response = requests.get(f"{base_url}/booking/{created_booking}")
        assert response.status_code == 404

    def test_delete_booking_without_auth_returns_403(self, base_url, created_booking):
        response = requests.delete(f"{base_url}/booking/{created_booking}")

        assert response.status_code == 403

    def test_delete_nonexistent_booking_returns_405(self, base_url, auth_token):
        # BUG-010: returns 405 instead of 404 for nonexistent booking
        response = requests.delete(
            f"{base_url}/booking/99999",
            headers={"Cookie": f"token={auth_token}"}
        )

        assert response.status_code == 405