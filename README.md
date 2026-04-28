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

2. Create and activate a virtual environment
A virtual environment ensures that the installed packages are only used for this project.

Create the virtual environment:

python -m venv env
Activate the virtual environment:

Windows
.\env\Scripts\Activate.ps1
Mac/Linux
source env/bin/activate
✅ You will know it worked when (env) appears at the beginning of your command line.

3. Install dependencies
Install all required packages from requirements.txt:

pip install -r requirements.txt
4. Set up the database
Since the project uses SQLite, you do not need to install a separate database.

Simply run:

python manage.py migrate
ℹ️ Running makemigrations is not necessary, because the migration files are already included in the project. migrate is enough.

5. Start the server
python manage.py runserver
The API will then be available at:

http://127.0.0.1:8000/
