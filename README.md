# EventAPI
## Table of Contents
- About the Project
- Features
- Technologies Used
- Installation
- Usage
- API Documentation

----------------------------------------------------------------------------

### About the Project
It is  a event management API for an admin panel. It supports role-based
access (Admin and User), event creation, and basic ticket purchases.

----------------------------------------------------------------------------

### Features
- User authentication with simple JWT
- User role based authorization
- RESTful API endpoints

----------------------------------------------------------------------------

### Technologies Used
- Django - Web Framework
- Django REST Framework (DRF) - API development
- MySQL - Database

----------------------------------------------------------------------------

### Installation
##### Prerequisites
Make sure you have the following installed on your system:
- Python (>= 3.8)
- pip (Python package installer)
- virtualenv (recommended)
#### Steps to Set Up the Project
1. Clone the repository:  git clone https://github.com/mukesh-pandey9017/EventAPI.git
2. Navigate to the project directory:  cd EventAPI
3. Create a virtual environment:  python -m venv venv
4. Activate the virtual environment
Windows:  venv\Scripts\activate
Mac/Linux:  source venv/bin/activate
5. Install dependencies:    pip install -r requirements.txt
6. Apply database migrations:    python manage.py migrate
7. Run the development server:    python manage.py runserver
8. Open your browser and navigate to http://127.0.0.1:8000.

----------------------------------------------------------------------------

### API Documentation
#### Endpoints
1. User Registration   
POST /api/register/    : Registers a new user.   
request body:
{
  "username":"",
  "password":"",
  "role":"Admin" / "User"
}

2. Loging User for JWT access token    
POST /api/login/   : login user.
request body:
{
  "username":"",
  "password":""
}

3. Create a Event
POST /api/events/  :  for create events it requires authenticated user as Admin role only
request body:
{
  "name":"",
  "total_tickets":""
}

5. List all Events
GET /api/events/  : for fetching events it requires authenticated user of any role

6. purchase ticket of event
POST /api/events/<int:id>/purchase/  : for purchasing ticket it it requires authenticated user as User role only
request body:
{
  "quantity":""
}
