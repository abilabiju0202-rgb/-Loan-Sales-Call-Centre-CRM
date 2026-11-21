🏦 Loan Sales & Call Centre CRM

Overview

The Loan Sales & Call Centre CRM is a web-based Customer Relationship Management application developed using Python and Django. It is designed to simplify and centralize the management of customer leads, employee activities, call records, follow-ups, and loan applications.

The system provides separate role-based access for Administrators and Staff, allowing administrators to manage employees, assign customer leads, monitor performance, configure banks and loan schemes, and track loan applications.

Staff members can manage their assigned leads, record customer calls, schedule follow-ups, create loan applications, and upload required documents through their dashboard.

The application aims to improve workflow efficiency, customer relationship management, employee productivity, and transparency in loan processing activities.

Features

👨‍💼 Admin Module

🔐 Secure Admin Login

📊 Admin Dashboard

👥 Employee Management (Add, Edit, View and Deactivate Employees)

📋 Customer Lead Management

📌 Individual Lead Assignment to Staff

📤 Bulk Customer Lead Upload using CSV

📞 Call Centre Activity Monitoring

📈 Employee Performance and Target Monitoring

🏦 Bank Management

💰 Loan Scheme Management

📄 Document Collection and Verification

📝 Loan Application Management

🔄 Loan Application Status Management

📊 Application and Lead Monitoring

📱 Responsive Admin Dashboard

👨‍💻 Staff Module

🔐 Secure Staff Login

📊 Staff Dashboard

📋 View Assigned Customer Leads

🔍 Search Customer Leads

📞 Record Customer Calls and Call Remarks

📌 Update Lead Status

📅 Schedule and Manage Follow-ups

🎯 Daily Call Target Tracking

📝 Create Loan Applications for Assigned Customers

📤 Upload Required Customer Documents

🔄 Track Loan Application Status

🔄 Loan Management Workflow

Admin adds customer leads or imports leads through CSV.

Admin assigns customer leads to staff members.

Staff contacts customers and records call details.

Staff updates lead status and schedules follow-ups.

Staff creates loan applications for assigned customers.

Required documents are uploaded and verified.

Administrators manage and update application statuses.

Loan applications are tracked through the processing stages, including approval, disbursement, and closure.

Technologies Used

Backend

Python

Django

Frontend

HTML5

CSS3

Bootstrap 5

JavaScript

Database

SQLite

Data Visualization

Chart.js

Tools

PyCharm

Visual Studio Code

Git

GitHub

Key Technical Implementations

Django ORM: Database operations using Django models.

Custom User Model: Role-based user management for Admin and Staff.

Authentication and Authorization: Secure login and access control based on user roles.

CRUD Operations: Create, Read, Update and Delete operations for employees, customer leads, banks and loan schemes.

CSV Processing: Bulk customer lead import using CSV files.

Form Validation: Server-side validation for user inputs and application data.

File Uploads: Customer document collection and management.

Dashboard Analytics: Displaying CRM activities and performance information.

Responsive Design: Bootstrap-based interface for different screen sizes.

Project Structure

loan-crm/
│
├── crm/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
├── static/
├── media/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md

Note: The project structure above illustrates the main Django components. Adjust folder and application names to match your actual repository.

Installation and Setup

1. Clone the Repository

git clone https://github.com/yourusername/loan-crm.git

2. Navigate to the Project Directory

cd loan-crm

3. Create a Virtual Environment

python -m venv venv

4. Activate Virtual Environment

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

5. Install Dependencies

pip install -r requirements.txt

6. Apply Database Migrations

python manage.py makemigrations
python manage.py migrate

7. Create an Administrator Account

python manage.py createsuperuser

8. Run the Development Server

python manage.py runserver

Open the application in your browser:

http://127.0.0.1:8000/

Future Enhancements

Integration with SMS and Email Notifications.

Advanced Performance Analytics and Reporting.

Automated Follow-up Reminders.

Loan EMI and Repayment Tracking.

Payment Gateway Integration.

Advanced Customer Communication Features.

Cloud Deployment and Hosting.

Learning Outcomes

This project provided hands-on experience in:

Python and Django Web Development.

Full-Stack Web Application Development.

Database Design and Management.

Django ORM and Model Relationships.

Authentication and Role-Based Access Control.

CRUD Operations and Form Handling.

CSV File Processing and Data Import.

File Upload and Document Management.

Application Testing and Debugging.

Responsive UI Development using Bootstrap.

Git and GitHub Version Control.

Implementing Real-World Business Workflows.

Author

Abila Biju

MCA Graduate

GitHub: https://github.com/abilabiju0202-rgb

