# Test Plan — Restful Booker API


**Project:** Restful Booker API Testing  
**API under test:** https://restful-booker.herokuapp.com  

---

## 1. Objective

The objective of this test plan is to document the testing strategy applied to the Restful Booker API — including what was tested, why, in what order, and how decisions were made about automation coverage.

---

## 2. Scope

All 8 endpoints of the Restful Booker API were in scope:

| Method | Endpoint | Priority |
|---|---|---|
| GET | `/ping` | High |
| POST | `/auth` | High |
| GET | `/booking` | High |
| GET | `/booking/:id` | High |
| POST | `/booking` | High |
| PUT | `/booking/:id` | High |
| DELETE | `/booking/:id` | High |
| PATCH | `/booking/:id` | Medium |

---

## 3. Testing Approach

### 3.1 Manual Exploratory Testing First

All endpoints were tested manually using Postman before any automation was written.

This decision was deliberate — documentation alone is not sufficient to understand real API behaviour. The Restful Booker documentation does not mention that `/ping` returns 201 instead of 200, or that `/auth` returns 200 for invalid credentials. These behaviours were only discovered through manual exploration.

**Lesson applied:** documentation is a starting point, not a source of truth. Always validate against the actual system.

### 3.2 Test Execution Order

Tests were executed in dependency order:

```
1. Health Check (GET /ping)
      ↓
2. Explore existing data (GET /booking, GET /booking/:id)
      ↓
3. Authentication (POST /auth)
      ↓
4. Create test data (POST /booking)
      ↓
5. Update operations (PUT, PATCH)
      ↓
6. Delete operations (DELETE)
```

**Rationale:**

- **Health Check first** — Smoke Test. If the API is down, there is no point testing anything else.
- **GET before POST** — exploring existing data reveals the JSON structure, field names, and data types before writing any payloads. Even with documentation available, manual exploration catches discrepancies between docs and real behaviour.
- **AUTH before write operations** — PUT, PATCH and DELETE require a valid token. Authentication must be validated before operations that depend on it.
- **POST before PUT/PATCH/DELETE** — resources must exist before they can be updated or deleted. This is a natural test dependency.
- **PATCH last** — PATCH is functionally redundant with PUT. If time is limited, PATCH is deprioritised.

---

## 4. Test Coverage

### 4.1 Scenarios Covered Per Endpoint

For each endpoint, the following scenario types were tested:

- **Happy path** — valid request with expected data
- **Negative testing** — invalid inputs, missing fields, wrong data types
- **Boundary testing** — edge values such as ID=0 and ID=99999
- **Authentication testing** — missing token, invalid token, wrong credentials
- **Data integrity** — response body matches what was sent in the request
- **Schema validation** — response contains expected fields with correct types
- **Confirmation testing** — after DELETE, a GET confirms the resource no longer exists

### 4.2 Risk-Based Prioritisation

With limited time, the priority order would be:

1. **POST /auth** — without authentication, write operations cannot be tested
2. **GET /booking** — validates basic read functionality
3. **POST /booking** — validates resource creation
4. **PUT /booking/:id** — validates full update
5. **DELETE /booking/:id** — validates resource deletion
6. **PATCH /booking/:id** — deprioritised as it overlaps with PUT functionality

**Rationale:** risk-based testing focuses on what has the highest business impact. PATCH is convenient but not critical — the system functions without it.

---

## 5. Automation Strategy

### 5.1 What Was Automated

All 29 test cases were automated using Python and Pytest.

### 5.2 Why Automate Everything

Since this is a portfolio project covering a stable, public API, full automation was appropriate. In a real project, the decision would weigh:

- **Automate:** stable endpoints, regression scenarios, repeated executions
- **Keep manual:** exploratory sessions, one-off validations, UI flows

### 5.3 Key Technical Decisions

**Fixtures for shared configuration**  
Base URL and authentication token are defined in `conftest.py`. If either changes, only one place needs to be updated.

**Dynamic test data instead of hardcoded IDs**  
Booking IDs are fetched at runtime. During development, a hardcoded ID broke when another user deleted that booking from the shared API. Dynamic data makes tests resilient to external changes.

**Yield fixtures for setup and teardown**  
Each test that requires a booking creates one in setup and deletes it in teardown. This ensures test isolation — no test depends on data left by another test.

**Bug documentation inline**  
Known bugs are documented with inline comments referencing the BUG_REPORT.md. This makes it clear the test is asserting current (buggy) behaviour, not expected behaviour.

**Tests organised in classes by endpoint**  
Each class represents a Test Suite for one endpoint. As the suite grows, each class can be moved to its own file without restructuring.

---

## 6. Defect Severity Criteria

| Severity | Criteria | Example |
|---|---|---|
| High | Security impact, data corruption, or silent failures in integrations | BUG-003: 200 for invalid credentials |
| Medium | Incorrect behaviour that misleads API consumers | BUG-006: 405 instead of 403 |
| Low | Minor inconsistency with minimal business impact | BUG-011: 405 on double DELETE |

---

## 7. What Was Not Tested

- **Performance / load testing** — out of scope for this phase
- **Security testing** — out of scope for this phase
- **Contract testing** — no schema validation tool (e.g. Pact) was used
- **UI testing** — API only

These areas would be covered in subsequent testing phases.

---

## 8. Tools

| Tool | Purpose |
|---|---|
| Postman | Manual exploratory testing |
| Python 3.13 | Automation language |
| Pytest | Test framework |
| Requests | HTTP library |
| Allure Pytest | Test reporting |
| GitHub Actions | CI/CD pipeline |

---

*This test plan documents decisions made during the testing process — not a pre-defined script, but a reflection of a real QA workflow.*