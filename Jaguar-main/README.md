# Music School Management System (MSMS)

## Team Members
The members of the team are:
- Aayush Dwivedi (aayush.dwivedi@kcl.ac.uk)
- Ronen Roy (ronen.roy@kcl.ac.uk)
- Oliver Singer (oliver.singer@kcl.ac.uk)
- Tony Smith (tony.o.smith@kcl.ac.uk)
- Kabir Suri (kabir.suri@kcl.ac.uk)

## Project Overview

The **Music School Management System (MSMS)** is a comprehensive Django web application designed to manage music lessons, student requests, teacher assignments, and financial transactions for a music school. The system provides role-based access control with three distinct user types: Students, Administrators, and Directors.

## Project Structure

The project is called `msms` (Music School Management System) and consists of a single Django app called `lessons` where all functionality resides. The project follows Django's standard structure with clear separation of concerns.

### Core Components

- **Models**: Define the data structure for users, lesson requests, lessons, teachers, terms, invoices, and payments
- **Views**: Handle user interactions and business logic for different user roles
- **Forms**: Manage data input validation and user interface
- **Templates**: Provide the HTML structure for the web interface
- **Static Files**: Contain CSS styling and images
- **Tests**: Comprehensive test suite covering models, forms, and views

## Key Features

### User Management
- **Custom User Model**: Email-based authentication with role-based access control
- **Three User Roles**:
  - **Students**: Can request lessons, view booked lessons, and manage invoices
  - **Administrators**: Can manage lesson requests, book lessons, and view student balances
  - **Directors**: Can manage administrators and oversee all system operations

### Lesson Management
- **Lesson Requests**: Students can submit detailed lesson requests including:
  - Availability for each day of the week (Monday-Friday)
  - Number of lessons desired
  - Lesson interval in days
  - Lesson duration in minutes
  - Additional information/notes
- **Lesson Booking**: Administrators can book lessons based on student requests
- **Teacher Assignment**: Lessons are assigned to specific teachers
- **Term Management**: Lessons are organized within academic terms

### Financial Management
- **Invoice Generation**: Automatic invoice creation for completed lesson requests
- **Payment Tracking**: Record and track student payments
- **Balance Calculation**: Real-time calculation of student account balances
- **Pricing**: Dynamic lesson pricing based on duration (multiplier: 1.15 per minute)

### Administrative Features
- **Student Balance Management**: View and manage student financial accounts
- **Administrator Management**: Directors can create, edit, and delete administrator accounts
- **Lesson Request Processing**: Comprehensive workflow for handling lesson requests
- **Data Seeding**: Management commands for populating the database with test data

## Technical Architecture

### Technology Stack
- **Backend**: Django 4.1.2 (Python web framework)
- **Database**: SQLite (development), easily configurable for production
- **Frontend**: HTML templates with CSS styling
- **Testing**: Django's built-in testing framework with comprehensive test coverage
- **Additional Packages**:
  - `django-widget-tweaks`: Enhanced form rendering
  - `Faker`: Test data generation
  - `coverage`: Test coverage analysis

### Database Schema

#### Core Models
1. **User**: Custom user model with email authentication and role-based access
2. **LessonRequest**: Student lesson requirements and preferences
3. **Lesson**: Individual lesson instances with teacher assignments
4. **Teacher**: Music instructors available for lessons
5. **Term**: Academic terms for organizing lessons
6. **Invoice**: Financial records for lesson requests
7. **Payment**: Student payment records

#### Key Relationships
- Users can have multiple lesson requests
- Lesson requests can generate multiple lessons
- Lessons are assigned to teachers and students
- Invoices are generated for lesson requests
- Payments are linked to invoices and users

### URL Structure
The application uses a hierarchical URL structure:
- `/` - Home page and authentication
- `/student/` - Student-specific functionality
- `/administrator/` - Administrator management features
- `/director/` - Director oversight and management

## Installation Instructions

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup Steps

1. **Clone the repository** and navigate to the project directory:
   ```bash
   cd Jaguar-main
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Seed the development database** with sample data:
   ```bash
   python manage.py seed
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application** at `http://127.0.0.1:8000/`

### Testing
Run the comprehensive test suite:
```bash
python manage.py test
```

### Database Management
- **Seed database**: `python manage.py seed`
- **Unseed database**: `python manage.py unseed`
- **Create migrations**: `python manage.py makemigrations`
- **Apply migrations**: `python manage.py migrate`

## User Workflows

### Student Workflow
1. **Registration**: Create account with email and personal details
2. **Login**: Access student dashboard
3. **Request Lessons**: Submit detailed lesson requests with preferences
4. **View Booked Lessons**: See confirmed lesson bookings
5. **Manage Invoices**: View and track payment status

### Administrator Workflow
1. **Login**: Access administrator dashboard
2. **Review Lesson Requests**: View and process student requests
3. **Book Lessons**: Assign teachers and schedule lessons
4. **Manage Student Balances**: Track financial accounts
5. **Process Payments**: Record student payments

### Director Workflow
1. **Login**: Access director dashboard
2. **Manage Administrators**: Create, edit, and delete admin accounts
3. **Oversee Operations**: Monitor lesson requests and student balances
4. **System Administration**: Full system access and management

## Security Features

- **Email-based Authentication**: Secure login system
- **Role-based Access Control**: Different permissions for each user type
- **CSRF Protection**: Built-in Django security features
- **Input Validation**: Comprehensive form validation
- **Secure Password Handling**: Django's built-in password security

## Development Features

### Code Quality
- **Comprehensive Testing**: Unit tests for models, forms, and views
- **Test Fixtures**: Predefined test data for consistent testing
- **Code Coverage**: Built-in coverage analysis
- **Form Validation**: Robust input validation and error handling

### Database Management
- **Migrations**: Version-controlled database schema changes
- **Seeding**: Automated test data generation
- **Fixtures**: JSON-based test data management

### User Interface
- **Responsive Design**: Clean, modern interface
- **Form Enhancements**: Improved form rendering with django-widget-tweaks
- **Visual Feedback**: Success and error message handling
- **Intuitive Navigation**: Role-based menu systems

## File Structure

```
Jaguar-main/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── msms/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
└── lessons/                 # Main application
    ├── models/              # Data models
    │   ├── user.py          # Custom user model
    │   ├── lesson_request.py # Lesson request model
    │   ├── lesson.py        # Lesson model
    │   ├── teacher.py       # Teacher model
    │   ├── term.py          # Term model
    │   ├── invoice.py       # Invoice model
    │   └── payment.py       # Payment model
    ├── views/               # View logic
    │   ├── administrator/   # Admin-specific views
    │   ├── director/        # Director-specific views
    │   ├── student/         # Student-specific views
    │   └── shared/          # Shared view components
    ├── forms/               # Form definitions
    ├── templates/           # HTML templates
    ├── static/              # CSS and images
    ├── tests/               # Test suite
    ├── management/          # Custom management commands
    └── migrations/          # Database migrations
```

## Deployment

The application is configured for development with SQLite database. For production deployment:

1. **Configure Production Database**: Update `settings.py` with production database settings
2. **Set Environment Variables**: Configure `SECRET_KEY` and other sensitive settings
3. **Static Files**: Configure static file serving
4. **Security Settings**: Update `DEBUG=False` and configure `ALLOWED_HOSTS`
5. **Web Server**: Deploy using WSGI-compatible server (e.g., Gunicorn)

## Sources and Acknowledgments

### Packages and Dependencies
- **Django**: Web framework (specified in `requirements.txt`)
- **django-widget-tweaks**: Enhanced form rendering
- **Faker**: Test data generation
- **coverage**: Test coverage analysis

### External Resources
- **Source Code**: Some components adapted from the Clucker project
- **Illustrations**: 
  - [Connected World illustration](https://storyset.com/illustration/connected-world/amico) from Storyset
  - Background images from Pinterest
- **CSS Resources**:
  - [W3Schools CSS](https://www.w3schools.com/Css/)
  - [CSS Button Examples](https://getcssscan.com/css-buttons-examples)

## Future Enhancements

Potential areas for future development:
- **Calendar Integration**: Visual lesson scheduling interface
- **Email Notifications**: Automated lesson reminders and confirmations
- **Payment Gateway Integration**: Online payment processing
- **Mobile Application**: Native mobile app for students and teachers
- **Advanced Reporting**: Comprehensive analytics and reporting features
- **Multi-language Support**: Internationalization capabilities

## Support and Maintenance

For technical support or questions about the Music School Management System, please contact the development team members listed above.

---

*This README provides a comprehensive overview of the Music School Management System. For specific implementation details, refer to the source code and inline documentation.*