# Django Project with Task Management and Workflow Automation

This Django-based project is built around managing tasks, users, and node operations within a structured workflow. It consists of **four apps**:

- `users`
- `task`
- `work_tower`
- `workflow`

The project emphasizes **low coupling**, **reusability**, and **automated workflows**, using tools like **Celery**, **Twilio**, and **Django signals**.

---

## 📦 Apps Overview

### 1. `users` App

Implements custom user logic based on **cell phone numbers** for authentication.

#### Key Features:
- Custom `CustomUser` model with `USERNAME_FIELD = 'cell_number'`
- Handles registration and login via:
  - `views.py` and `forms.py`
- Dedicated employee logic via:
  - `employee_views.py` and `employee_forms.py`
- Context processor for injecting employee-related context into templates
- Custom user manager for filtering by role (e.g., `get_electricians_view()`)

---

### 2. `task` App

Manages the full **task lifecycle**, including archiving and deadline management.

#### Key Features:
- Models:
  - `Task`
  - `TaskArchive` (receives completed tasks via signals)
- Business logic:
  - If a `Task` status is set to `COMPLETED`, it is automatically moved to `TaskArchive`
- Deadline checking:
  - Uses [`django_celery_beat`](https://github.com/celery/django-celery-beat) to check for expired deadlines every 60 seconds
- Management commands:
  - Automatically reset expired tasks (status changed to `PENDING`, deadline cleared)

---

### 3. `work_tower` App

Contains the **core business logic** related to nodes (data units or process points).

#### Key Features:
- Create, retrieve, update, sort, and delete **nodes**
- Nodes are used to associate tasks and provide operational hierarchy

---

### 4. `workflow` App

Implements a decoupled **task assignment system** between `users` and `task` apps.

#### Key Features:
- Assigns tasks to employees via:
  - Function-based views
  - Django signals
- Sends SMS notifications to the assigned user using [`django-twilio`](https://github.com/ui/django-twilio)
- Keeps user-task interaction loosely coupled and maintainable

---

## 🧪 Testing Strategy

- Function-based views are used throughout the project for **easier testing and readability**
- Tests cover:
  - View logic
  - Authentication
  - Task transitions
  - Signal-based actions
  - Management commands

---

## ⚙️ Tech Stack

- Django
- Celery + django-celery-beat
- Twilio (via `django-twilio`)
- PostgreSQL
- Python `>=3.8`

---
