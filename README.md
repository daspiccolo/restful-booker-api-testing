# Restful Booker API Testing

[![API Tests](https://github.com/daspiccolo/restful-booker-api-testing/actions/workflows/tests.yml/badge.svg)](https://github.com/daspiccolo/restful-booker-api-testing/actions/workflows/tests.yml)

Exploratory and automated API testing project for the [Restful Booker API](https://restful-booker.herokuapp.com).

This project follows a real QA workflow — starting with manual exploratory testing to understand the API behaviour and document bugs, followed by test automation with Python and Pytest.

---

## Project Structure

```
restful-booker-api-testing/
│
├── .github/
│   └── workflows/
│       └── tests.yml        ← CI pipeline with GitHub Actions
├── tests/
│   └── api/
│       └── test_bookings.py ← automated test suites
├── conftest.py              ← shared fixtures and configuration
├── requirements.txt         ← project dependencies
├── BUG_REPORT.md            ← 11 bugs found during manual testing
└── README.md
```

---

## Phase 1 — Manual Exploratory Testing ✅

All endpoints were tested manually using Postman before any automation was written. This phase focused on understanding the expected behaviour of each endpoint, including edge cases and negative scenarios.

**Endpoints tested:**

| Method | Endpoint | Description |
|---|---|---|
| GET | `/ping` | Health check |
| GET | `/booking` | Get all bookings — including filters |
| GET | `/booking/:id` | Get booking by ID |
| POST | `/auth` | Generate authentication token |
| POST | `/booking` | Create a new booking |
| PUT | `/booking/:id` | Full update of a booking |
| PATCH | `/booking/:id` | Partial update of a booking |
| DELETE | `/booking/:id` | Delete a booking |

**Scenarios covered per endpoint:**
- Happy path
- Missing or invalid fields
- Wrong data types
- Invalid or non-existent IDs
- Unauthenticated requests
- Duplicate operations

**Result: 11 bugs documented** — see [BUG_REPORT.md](./BUG_REPORT.md)

---

## Phase 2 — Test Automation ✅

29 automated tests covering all 8 endpoints, organised by Test Suite.

**Tech stack:**
- Python 3.13
- Pytest
- Requests
- Allure Pytest
- GitHub Actions

**Test Suites:**

| Suite | Endpoint | Tests |
|---|---|---|
| TestHealthCheck | GET /ping | 2 |
| TestGetAllBookings | GET /booking | 4 |
| TestGetBookingById | GET /booking/:id | 4 |
| TestAuth | POST /auth | 3 |
| TestCreateBooking | POST /booking | 5 |
| TestUpdateBooking | PUT /booking/:id | 4 |
| TestPartialUpdateBooking | PATCH /booking/:id | 4 |
| TestDeleteBooking | DELETE /booking/:id | 4 |
| **Total** | | **29** |

**Key implementation decisions:**

- Fixtures in `conftest.py` centralise base URL and authentication token — if either changes, only one place needs updating
- Dynamic test data — booking IDs are fetched at runtime instead of hardcoded, making tests resilient to external changes
- Yield fixtures for setup and teardown — each test creates its own booking and deletes it after, ensuring test isolation
- Known bugs are documented inline with comments referencing the BUG_REPORT.md

---

## CI/CD Pipeline

Tests run automatically on every push and pull request to `main` via GitHub Actions.

The pipeline runs on a clean Ubuntu environment, ensuring tests pass regardless of local machine configuration.

---

## How to Run Locally

```bash
# clone the repository
git clone https://github.com/daspiccolo/restful-booker-api-testing.git
cd restful-booker-api-testing

# create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# install dependencies
pip install -r requirements.txt

# run all tests
pytest tests/ -v

# generate Allure report
pytest tests/ -v --alluredir=allure-results
allure serve allure-results
```

---

## Key Findings

During exploratory testing, the following systemic issues were identified across the API:

- **Widespread misuse of 405** — used incorrectly for authentication failures and missing resources instead of 403 and 404
- **Missing input validation** — POST and PATCH accept missing fields, wrong data types, and invalid date ranges without error
- **Inconsistent authentication errors** — PUT and PATCH return different status codes for the same unauthenticated scenario
- **500 error caused by invalid input** — invalid client input should always return 4xx, never 5xx

Full details in [BUG_REPORT.md](./BUG_REPORT.md)

---

*Tested by Debora Piccolo — QA Engineer*