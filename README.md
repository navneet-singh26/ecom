# E-commerce Data Management and User Authentication System

## Overview

This Django-based project manages product data for an e-commerce platform, including data upload, cleaning, and summary report generation. It also includes a simple user authentication system with JWT-based login and sign-up functionality.

## Features

- **Product Data Management**: Upload and clean product data from a CSV file.
- **User Authentication**: Sign-up and login functionality with JWT token-based authentication.
- **Data Cleaning**: Handle missing values and ensure data integrity.
- **Summary Report**: Generate a CSV report of total revenue, top product, and top quantity sold per category.

## Technologies Used

- **Django**: Web framework used for developing the project.
- **SQLite**: Default database used (can be replaced with PostgreSQL, MySQL, etc.).
- **PyJWT**: Library used for creating and verifying JWT tokens.
- **bcrypt**: Library used for password hashing and verification.
- **Pandas**: Used for data processing and cleaning.


## Setup Instructions

### Prerequisites

- Python 3.10
- pip (Python package installer)
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/ecommerce.git
   cd ecommerce

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   
5. **Run the development server**:
   ```bash
   python manage.py runserver
   
### Setting Up the Product Data

1. **Prepare your CSV file**:

   Ensure your CSV file contains the following columns:

   - `product_id`
   - `product_name`
   - `category`
   - `price`
   - `quantity_sold`
   - `rating`
   - `review_count`

2. **Upload product data**:
   ```bash
   python manage.py upload_data --filepath=path/to/your/products.csv

### User Authentication

1. **Sign Up**:

   - **Endpoint**: `POST /products/signup/`
   - **Request Body**:
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```

2. **Login**:

   - **Endpoint**: `POST /products/login/`
   - **Request Body**:
     ```json
     {
       "username": "your_username",
       "password": "your_password"
     }
     ```
   - **Response**:
     ```json
     {
       "token": "your_jwt_token"
     }
     ```
     - The response will include a JWT token if the login is successful.

### Generating the Summary Report

1. **Access the summary report** by visiting the following URL:

   ```bash
   http://127.0.0.1:8000/products/summary_report/
   ```
   This will generate and download a CSV file with the following columns:
   
   - `category`
   - `total_revenue`
   - `top_product`
   - `top_product_quantity_sold`