# 📦 Coderr Backend
A RESTful backend API for a freelancer developer platform, built with Django REST Framework.

The backend handles all core functionalities such as user management, project handling, bookings, and communication between clients and developers.  
It is designed to integrate seamlessly with an existing frontend application.

## 🛠️ Requirements
Make sure the following is installed on your computer:

- Python 3.12
- Git

## 🚀 Installation – Step by Step

### 1. Clone the repository
Open your terminal (or command prompt) and run:

```bash
git clone https://github.com/your-username/coderr-backend.git
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
```

**Windows:**
```bash
.\env\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

```bash
python manage.py migrate
```

### 5. Start the server

```bash
python manage.py runserver
```

The API will then be available at: http://127.0.0.1:8000/