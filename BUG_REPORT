# Bug Report — Restful Booker API


**Environment:** https://restful-booker.herokuapp.com  
**Testing type:** Manual — Exploratory  
**Tool:** Postman  

---

## Summary

| # | Endpoint | Severity | Status |
|---|---|---|---|
| BUG-001 | GET /booking | Medium | Open |
| BUG-002 | GET /booking/:id | Low | Open |
| BUG-003 | POST /auth | High | Open |
| BUG-004 | POST /booking | High | Open |
| BUG-005 | POST /booking | High | Open |
| BUG-006 | PUT /booking/:id | Medium | Open |
| BUG-007 | PUT /booking/:id | Medium | Open |
| BUG-008 | PUT vs PATCH | Medium | Open |
| BUG-009 | PATCH /booking/:id | Medium | Open |
| BUG-010 | DELETE /booking/:id | Medium | Open |
| BUG-011 | DELETE /booking/:id | Low | Open |

---

## Bug Details

---

### BUG-001 — GET /booking accepts invalid date format without error

**Endpoint:** `GET /booking`  
**Severity:** Medium  
**Priority:** Medium  

**Description:**  
The API accepts date parameters in any format without returning a validation error. This can cause unexpected results for API consumers who send dates in the wrong format.

**Steps to reproduce:**
1. `GET /booking?checkin=01-01-2024`
2. Observe the response

**Expected result:** `400 Bad Request` with message `"Invalid date format. Use YYYY-MM-DD"`  
**Actual result:** `200 OK` with a list of results

**Notes:** Only the format `YYYY-MM-DD` is documented as valid. Other formats should be rejected.

---

### BUG-002 — GET /booking/:id returns 404 for non-numeric IDs instead of 400

**Endpoint:** `GET /booking/:id`  
**Severity:** Low  
**Priority:** Low  

**Description:**  
When a non-numeric value is passed as the booking ID, the API returns 404 Not Found instead of 400 Bad Request. The server should reject invalid input before attempting to find the resource.

**Steps to reproduce:**
1. `GET /booking/abc`
2. Observe the response

**Expected result:** `400 Bad Request`  
**Actual result:** `404 Not Found`

**Notes:** 404 means "I looked and didn't find it." For an invalid input like `abc`, the server shouldn't look at all — it should reject it immediately with 400.

---

### BUG-003 — POST /auth returns 200 for invalid credentials instead of 401

**Endpoint:** `POST /auth`  
**Severity:** High  
**Priority:** High  

**Description:**  
When invalid credentials are provided, the API returns `200 OK` with `{"reason": "Bad credentials"}` in the body instead of `401 Unauthorized`. This is a critical design issue — any system that checks only the status code will incorrectly assume authentication succeeded.

**Steps to reproduce:**
1. `POST /auth`
2. Body: `{"username": "admin", "password": "wrongpassword"}`
3. Observe the response

**Expected result:** `401 Unauthorized`  
**Actual result:** `200 OK` with body `{"reason": "Bad credentials"}`

**Notes:** This is a semantic HTTP violation. Status 200 communicates success. Returning 200 for a failed authentication can cause silent failures in integrations.

---

### BUG-004 — POST /booking creates bookings with missing or invalid fields

**Endpoint:** `POST /booking`  
**Severity:** High  
**Priority:** High  

**Description:**  
The API accepts and creates bookings even when required fields are missing, field types are wrong, or check-in date is after check-out date. No input validation is applied.

**Steps to reproduce:**
1. `POST /booking` without `firstname` field → `200 OK`, booking created
2. `POST /booking` with `totalprice: "one hundred"` (string instead of number) → `200 OK`, booking created
3. `POST /booking` with `checkin` date after `checkout` date → `200 OK`, booking created

**Expected result:** `400 Bad Request` with a descriptive validation message in all cases  
**Actual result:** `200 OK` — booking created with corrupted or incomplete data

**Notes:** This allows corrupt data to enter the database, which can cause downstream failures.

---

### BUG-005 — POST /booking returns 500 for empty body instead of 400

**Endpoint:** `POST /booking`  
**Severity:** High  
**Priority:** High  

**Description:**  
Sending an empty body `{}` to the create booking endpoint causes a 500 Internal Server Error. Invalid client input should never cause a server error — it should be caught and returned as a 400.

**Steps to reproduce:**
1. `POST /booking`
2. Body: `{}`
3. Observe the response

**Expected result:** `400 Bad Request`  
**Actual result:** `500 Internal Server Error`

**Notes:** A 500 response to invalid input suggests the API lacks proper error handling internally. This can expose implementation details and makes debugging harder for consumers.

---

### BUG-006 — PUT /booking/:id returns 405 instead of 403 when unauthenticated

**Endpoint:** `PUT /booking/:id`  
**Severity:** Medium  
**Priority:** Medium  

**Description:**  
When a PUT request is made without authentication, the API returns `405 Method Not Allowed` instead of `403 Forbidden`. This is semantically incorrect — the method is valid, but the request lacks authorisation.

**Steps to reproduce:**
1. `PUT /booking/:id` without Authorization header
2. Observe the response

**Expected result:** `403 Forbidden`  
**Actual result:** `405 Method Not Allowed`

---

### BUG-007 — PUT /booking/:id returns 405 for non-existent ID instead of 404

**Endpoint:** `PUT /booking/:id`  
**Severity:** Medium  
**Priority:** Medium  

**Description:**  
When a valid PUT request is made with a non-existent booking ID, the API returns `405 Method Not Allowed` instead of `404 Not Found`.

**Steps to reproduce:**
1. `PUT /booking/99999` with valid authentication and complete body
2. Observe the response

**Expected result:** `404 Not Found`  
**Actual result:** `405 Method Not Allowed`

---

### BUG-008 — PUT and PATCH return inconsistent status codes for unauthenticated requests

**Endpoint:** `PUT /booking/:id` and `PATCH /booking/:id`  
**Severity:** Medium  
**Priority:** Medium  

**Description:**  
The same scenario — request without authentication — returns different status codes depending on the HTTP method used. This inconsistency makes error handling harder for API consumers.

**Steps to reproduce:**
1. `PUT /booking/:id` without authentication → `405 Method Not Allowed`
2. `PATCH /booking/:id` without authentication → `403 Forbidden`

**Expected result:** Both should return `403 Forbidden`  
**Actual result:** Different status codes for the same error condition

---

### BUG-009 — PATCH /booking/:id accepts empty body and unknown fields without error

**Endpoint:** `PATCH /booking/:id`  
**Severity:** Medium  
**Priority:** Medium  

**Description:**  
The PATCH endpoint accepts an empty body `{}` and unknown fields like `{"color": "blue"}` without returning a validation error. Both cases return 200 OK with no changes applied.

**Steps to reproduce:**
1. `PATCH /booking/:id` with body `{}` → `200 OK`
2. `PATCH /booking/:id` with body `{"color": "blue"}` → `200 OK`

**Expected result:** `400 Bad Request` — at minimum a warning that no valid fields were provided  
**Actual result:** `200 OK` with no changes and no feedback

---

### BUG-010 — DELETE /booking/:id returns 405 for non-existent ID instead of 404

**Endpoint:** `DELETE /booking/:id`  
**Severity:** Medium  
**Priority:** Medium  

**Description:**  
When attempting to delete a booking with a non-existent ID, the API returns `405 Method Not Allowed` instead of `404 Not Found`.

**Steps to reproduce:**
1. `DELETE /booking/99999` with valid authentication
2. Observe the response

**Expected result:** `404 Not Found`  
**Actual result:** `405 Method Not Allowed`

---

### BUG-011 — DELETE /booking/:id returns 405 when deleting an already deleted booking

**Endpoint:** `DELETE /booking/:id`  
**Severity:** Low  
**Priority:** Low  

**Description:**  
Attempting to delete a booking that has already been deleted returns `405 Method Not Allowed` instead of `404 Not Found`.

**Steps to reproduce:**
1. `DELETE /booking/:id` with valid authentication → `201 Created` (booking deleted)
2. `DELETE /booking/:id` again with the same ID → `405 Method Not Allowed`
3. `GET /booking/:id` → `404 Not Found` (confirms booking no longer exists)

**Expected result:** `404 Not Found` on the second DELETE  
**Actual result:** `405 Method Not Allowed`

---

## Patterns Observed

During exploratory testing, the following systemic issues were identified:

**1. Widespread misuse of 405 Method Not Allowed**  
Status 405 is used across multiple endpoints to communicate authentication failures, missing resources, and duplicate operations. The correct codes in these cases are 403 and 404 respectively.

**2. Missing input validation on write operations**  
POST and PATCH endpoints accept missing fields, wrong data types, invalid date ranges, and unknown fields without returning errors. This allows corrupt data to be persisted.

**3. Inconsistent authentication error handling**  
PUT returns 405 for unauthenticated requests while PATCH returns 403 for the same scenario. Authentication errors should be handled consistently across all endpoints.

**4. 500 errors caused by invalid client input**  
Client input errors should always return 4xx codes. A 500 response to an empty body suggests missing server-side error handling.

---

*Generated from manual exploratory testing session — Restful Booker API v1*
