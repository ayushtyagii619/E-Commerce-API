# E-Commerce Platform API - README
## Project Overview
This is a Django-based REST API for an e-commerce platform that allows sellers to list products, buyers to add items to their cart, place orders, and leave reviews. The API supports JWT authentication and ensures access control based on user roles (admin, seller, or buyer).

### Key Features
- User Authentication: Register, login, and profile management.
- Product Management: Sellers can create, update, and delete products.
- Cart Management: Users can add, update, and remove items from their cart.
- Order Management: Place and manage orders, track order status.
- Review System: Users can leave and update reviews on products.
- Role-based Permissions: Only sellers can manage products, and only the reviewer can manage their reviews.

### Tech Stack
- Backend: Django, Django REST Framework
- Authentication: JWT (JSON Web Tokens)
- Database: SQLite (default, can be swapped for PostgreSQL/MySQL)
- Media Handling: Django's built-in file storage system
- API Documentation: DRF Documentation

### Setup and Installation
### Prerequisites
- Python 3.x
- Django 4.x
- Django REST Framework
- djangorestframework-simplejwt
### Steps to Install
1. ### Clone the Repository:
git clone https://github.com/your-repo/ecommerce-api.git
cd ecommerce-api

2. ### Create a Virtual Environment:
python -m venv venv
source venv/bin/activate   # On Windows, use: venv\Scripts\activate

3. ### Install the Required Dependencies:
pip install -r requirements.txt

4. ### Run Migrations:
python manage.py migrate

5. ### Create a Superuser (Optional for Admin Access):
python manage.py createsuperuser

6. ### Run the Development Server:
python manage.py runserver

7. ### Access the Admin Panel:
   Visit http://127.0.0.1:8000/admin/ and log in with the superuser credentials.
