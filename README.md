Secure Password Platform
A secure password management platform built with Flask and SQLite. This platform allows users to store, manage, and share passwords securely.

Features
User Authentication:

Register, log in, and manage your account securely.

Password hashing using bcrypt for enhanced security.

Password Management:

Add, edit, view, and delete passwords.

Passwords are encrypted before being stored in the database.

Password Sharing:

Share passwords securely with other users.

Set expiry times and generate unique tokens for shared passwords.

Expiry Tracking:

Automatically track and display the status of shared passwords (Active, Expired, Used).

Password Strength Check:

Uses zxcvbn to evaluate password strength and provide feedback.

Rate Limiting:

Protects against brute force attacks with rate limiting on sensitive routes.

Screenshots
Dashboard
Dashboard
The dashboard displays your saved passwords and shared passwords.

Add Password
Add Password
Add a new password with site name, URL, and credentials.

Shared Passwords
Shared Passwords
View and manage shared passwords with expiry and usage status.

Installation
Prerequisites
Python 3.8 or higher

Pip (Python package manager)

Steps
Clone the repository:


git clone https://github.com/OCHHQ/secure_pass_platform.git


cd secure_pass_platform
Create a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

pip install -r requirements.txt
Set up the database:

Initialize the SQLite database:


flask db init
flask db migrate
flask db upgrade
Set environment variables:

Create a .env file in the root directory and add the following:


SECRET_KEY=your-secure-secret-key
DATABASE_URL=sqlite:///app.db
Run the application:


flask run
The app will be available at http://127.0.0.1:5000.

Usage
Register a new account:

Visit the registration page and create a new account.

Log in:

Use your credentials to log in to the platform.

Add a password:

Navigate to the "Add Password" page and enter the site name, URL, and password.

View and manage passwords:

Use the dashboard to view, edit, or delete your saved passwords.

Share a password:

Select a password to share, set an expiry time, and generate a unique token.

Track shared passwords:

View the status of shared passwords (Active, Expired, Used) on the dashboard.

Project Structure
collins@DESKTOP-KF14KQN:/mnt/c/Users/COLLINS$ tree /F secure_pass_platform -I "venv|__pycache__|.git" -L 2
/F  [error opening dir]
secure_pass_platform
├── README.md
├── app
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   └── services.py
├── decrypt_with_scrypt.py
├── init_db.py
├── instance
│   └── app.db
├── migrate_passwords.py
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── migrations_backup
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── requirements.txt
├── run.py
├── secret.key
├── static
│   ├── assets
│   └── styles.css
├── templates
│   ├── add_password.html
│   ├── base.html
│   ├── dashboard.html
│   ├── enable_2fa.html
│   ├── forgot_password.html
│   ├── home.html
│   ├── import_passwords.html
│   ├── login.html
│   ├── share_password.html
│   ├── share_password_success.html
│   ├── signup.html
│   ├── view_password.html
│   └── view_shared_password.html
├── test_app.py
├── test_decryption.py
└── test_services.py

10 directories, 38 files
collins@DESKTOP-KF14KQN:/mnt/c/Users/COLLINS$

Flask-Login: User authentication and session management.

Flask-WTF: Form handling and validation.

Flask-SQLAlchemy: Database ORM.

Flask-Migrate: Database migrations.

Flask-Limiter: Rate limiting for routes.

bcrypt: Password hashing.

zxcvbn: Password strength evaluation.

Contributing
Contributions are welcome! Here’s how you can contribute:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeatureName).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Flask for providing a lightweight and flexible web framework.

SQLite for a simple and efficient database solution.

zxcvbn for password strength evaluation.

Contact
For questions or feedback, feel free to reach out:

Email: enosejecollins@gmail.com

GitHub: ochhq