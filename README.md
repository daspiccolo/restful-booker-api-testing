# Restful Booker API Testing

Exploratory and automated API testing project for the [Restful Booker API](https://restful-booker.herokuapp.com).

This project follows a real QA workflow — starting with manual exploratory testing to understand the API behaviour and document bugs, followed by test automation with Python and Pytest.

---

## Project Structure

```
restful-booker-api-testing/
│
├── BUG_REPORT.md        ← 11 bugs found during manual testing
├── README.md
└── tests/               ← coming soon — automated tests in Python
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

## Key Findings

During exploratory testing, the following systemic issues were identified across the API:

- **Widespread misuse of 405** — used incorrectly for authentication failures and missing resources instead of 403 and 404
- **Missing input validation** — POST and PATCH accept missing fields, wrong data types, and invalid date ranges without error
- **Inconsistent authentication errors** — PUT and PATCH return different status codes for the same unauthenticated scenario
- **500 error caused by empty body** — invalid client input should always return 4xx, never 5xx

---

## Phase 2 — Test Automation 🚧 Coming Soon

The manual test cases will be automated using:

- **Python** — main language
- **Pytest** — test framework
- **Requests** — HTTP library
- **Allure** — test reports
- **GitHub Actions** — CI/CD pipeline

---

## How to Run (coming soon)

```bash
# install dependencies
pip install -r requirements.txt

# run all tests
pytest tests/ -v

# run with Allure report
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

---

## About This Project

This project was built as part of a QA automation portfolio. The goal was to apply a real QA process — explore manually, document findings, then automate — rather than jumping straight to writing scripts without understanding the system under test.

---

*Tested by Debora Piccolo — QA Engineer*
