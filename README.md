# Finance Dashboard System

A role-based backend system for managing financial records, generating dashboard analytics, and storing analyst insights.

This project was built with **Django** and **Django REST Framework** for:
- user and role management
- financial record CRUD operations
- dashboard summaries and trends
- analyst-written insights
- search, filtering, pagination, bulk operations, logging, and Swagger documentation

## Live API Documentation

**https://finance-dashboard-system-wptx.onrender.com/api/docs/**

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- JWT-based authentication
- File-based logging

---

# Project Structure

```text
finance-dashboard-system/
│
├── finance_dashboard/        # Main Django project settings and root URLs
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── users/                    # User management, login, roles, permissions
├── records/                  # Financial records CRUD, list, search, bulk create
├── dashboard/                # Summary, category breakdown, monthly trends
├── insights/                 # Analyst-created insights and bulk insight create
├── logs/                     # Application and activity logs
├── manage.py
├── requirements.txt
└── README.md
```

---

# Applications Overview

## Users App
Responsible for authentication, user management, and role handling.

### Main features
- create users
- list users
- retrieve user details
- update users
- delete users
- login using username and password
- role-based access control

### Roles
- **Admin**
- **Analyst**
- **Viewer**

### Access model
- **Admin**: manages users and record modification
- **Analyst**: accesses records, dashboard, and insights
- **Viewer**: read-oriented access to analytical endpoints

---

## Records App
The core business module of the project.

Each record represents one financial entry.

### Record fields
- amount
- type (`income` / `expense`)
- category
- date
- notes
- created_by
- updated_by
- created_at
- updated_at

### Main features
- create record
- retrieve record
- update record
- delete record
- list records with filters
- search records
- bulk create records
- pagination support

### Filtering and search
The records list API supports:
- `type`
- `category`
- `start_date`
- `end_date`
- `search`

Search works across:
- type
- category
- notes

---

## Dashboard App
Provides analytical APIs derived from records.

### Main endpoints
- **Summary API**: total income, total expense, net balance
- **Category Breakdown API**: totals grouped by category and type
- **Trend API**: month-wise trends by record date

### Purpose
This app does not store primary data. It computes analytical results from the `Record` model.

---

## Insights App
Stores analyst-created observations based on financial data.

### Main features
- list all insights
- list my insights
- retrieve an insight
- delete my own insight
- search and filter insights
- bulk create insights

### Insight fields
- title
- description
- created_by
- created_at

This app separates **human interpretation** from **computed analytics**.

---

# Key Features

## Role-Based Access Control
Custom permission classes are used to control access at the API level.

Examples:
- admin-only user management
- analyst/admin access for records and insights
- wider read access for dashboard endpoints where appropriate

---

## JWT-Based Authentication
The system uses JWT-based login.

### Login flow
1. User submits username and password
2. Backend validates credentials
3. JWT token is generated
4. Token is returned in the response
5. Token is also stored in a cookie for browser-based access

### Important Swagger note
Swagger UI may not automatically use the login cookie flow exactly like a normal browser app. For testing:
1. call `/users/login/`
2. use the returned token / authenticated session
3. test protected APIs

---

## Validation and Error Handling
Validation is handled primarily through serializers and controlled exceptions.

The backend uses meaningful status codes:
- `400` for invalid input
- `401` for missing/expired authentication
- `403` for insufficient permissions
- `404` for missing resources
- `500` for unexpected failures

This is important for a finance-related backend because request failures should be explicit and understandable.

---

## Search and Filtering
Both records and insights support practical retrieval filters.

### Records
- type
- category
- date range
- free-text search

### Insights
- creator
- date range
- free-text search

---

## Bulk Create Support
Bulk APIs are included for:
- records
- insights

This makes the backend more practical for seeded demo data and real usage scenarios.

---

## Pagination
List APIs support pagination so large result sets remain manageable.

---

## Logging
The project includes file-based logging.

### Logs folder
Please review the **`logs/`** folder.

Typical files:
- `app.log` – unexpected application/system errors
- `auth.log` – authentication activity
- `record_activity.log` – record create/update/delete actions
- `insight_activity.log` – insight activity

This was added because finance systems benefit from traceability and operational visibility.

---

## Swagger Documentation
Interactive API documentation is available through Swagger.

### Live Swagger URL
**https://finance-dashboard-system-wptx.onrender.com/api/docs/**

Swagger was added using `drf-spectacular` and helps with:
- endpoint discovery
- request/response inspection
- interactive testing

---

# Main API Groups

## Users
- `POST /users/create/`
- `GET /users/list/`
- `GET /users/detail/<username>/`
- `PATCH /users/update/<username>/`
- `DELETE /users/delete/<username>/`
- `POST /users/login/`

## Records
- `POST /records/create/`
- `GET /records/view/<pk>/`
- `PATCH /records/update/<pk>/`
- `DELETE /records/delete/<pk>/`
- `GET /records/list/`
- `POST /records/bulk-create/`

## Dashboard
- `POST /dashboard/summary/`
- `GET /dashboard/category/`
- `GET /dashboard/trend/`

## Insights
- `GET /insights/list/`
- `GET /insights/my-insights/`
- `GET /insights/view/<pk>/`
- `DELETE /insights/delete/<pk>/`
- `GET /insights/filter-list/`
- `POST /insights/bulk-create/`

---

# How to Run Locally

## 1. Clone the repository
```bash
git clone <your-repository-url>
cd finance-dashboard-system
```

## 2. Create and activate virtual environment
```bash
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

### macOS / Linux
```bash
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Run the server
```bash
python manage.py runserver
```

## 6. Open Swagger
```text
http://127.0.0.1:8000/api/docs/
```

---

# How to Access and Test

## Local Swagger
```text
http://127.0.0.1:8000/api/docs/
```

## Live Swagger
```text
https://finance-dashboard-system-wptx.onrender.com/api/docs/
```

## Recommended test flow
1. Create or use an existing user
2. Login using `/users/login/`
3. Use the returned token / authenticated session
4. Test records, dashboard, and insights APIs

---


# Notes for Reviewers

- Please review the **`logs/`** folder to see how activity and errors are recorded.
- Please use **Swagger UI** for the easiest way to explore and test the APIs.
- The project focuses on **clean structure, validation, access control, analytics, and practical backend behavior**, not only basic CRUD.

---

# Author

Backend implementation for a role-based finance dashboard system using Django REST Framework.
