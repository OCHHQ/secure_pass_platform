from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Password, SharedPassword, db
from datetime import datetime, timedelta
import secrets
from sqlalchemy.exc import IntegrityError
from . import bcrypt  # Import bcrypt from the app package

main = Blueprint('main', __name__)

# Generate a unique token for sharing
def generate_token():
    return secrets.token_urlsafe(32)

# Home Route
@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

# Register Route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('main.register'))
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('main.register'))
        
        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user
        new_user = User(username=username, email=email, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('main.register'))
    
    return render_template('signup.html')

# Login Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print(f"Email entered: {email}")  # Debug: Print the email entered
        print(f"Password entered: {password}")  # Debug: Print the password entered
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            print(f"User found: {user.username}")  # Debug: Print the username of the found user
            print(f"Stored password hash: {user.password}")  # Debug: Print the stored password hash
            
            # Verify the password using bcrypt
            if bcrypt.check_password_hash(user.password, password):
                print("Password matches! Logging in...")  # Debug: Confirm password match
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                print("Password does not match.")  # Debug: Confirm password mismatch
                flash('Login failed. Check your email and password.', 'danger')
        else:
            print(f"No user found with email: {email}")  # Debug: Confirm no user found
            flash('Login failed. Check your email and password.', 'danger')
    
    return render_template('login.html')

# Dashboard Route
@main.route('/dashboard')
@login_required
def dashboard():
    # Get the page number from the query string (default to 1)
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of passwords per page

    # Fetch passwords for the current user with pagination
    passwords = Password.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)

    # Fetch shared passwords for the current user
    shared_passwords = SharedPassword.query.join(Password).filter(Password.user_id == current_user.id).all()

    # Pass the pagination object, shared passwords, and datetime module to the template
    return render_template(
        'dashboard.html',
        passwords=passwords.items,
        shared_passwords=shared_passwords,
        page=page,
        total_pages=passwords.pages,
        datetime=datetime  # Pass the datetime module to the template
    )

# Logout Route
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

# Add Password Route
@main.route('/add_password', methods=['GET', 'POST'])
@login_required
def add_password():
    if request.method == 'POST':
        site_name = request.form.get('site_name')
        site_url = request.form.get('site_url')
        site_password = request.form.get('site_password')
        
        # Validate input
        if not site_name or not site_password:
            flash('Site name and password are required.', 'danger')
            return redirect(url_for('main.add_password'))
        
        # Encrypt the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(site_password).decode('utf-8')
        
        # Create new password entry
        password = Password(
            user_id=current_user.id,
            site_name=site_name,
            site_url=site_url,
            site_password=hashed_password
        )
        
        try:
            db.session.add(password)
            db.session.commit()
            flash('Password added successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while adding the password.', 'danger')
            return redirect(url_for('main.add_password'))
    
    return render_template('add_password.html')

# Edit Password Route
@main.route('/edit_password/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_password(id):
    password = Password.query.get_or_404(id)
    
    # Ensure the password belongs to the current user
    if password.user_id != current_user.id:
        flash('Access denied. You cannot edit this password.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        site_name = request.form.get('site_name')
        site_url = request.form.get('site_url')
        site_password = request.form.get('site_password')
        
        # Validate input
        if not site_name or not site_password:
            flash('Site name and password are required.', 'danger')
            return redirect(url_for('main.edit_password', id=id))
        
        # Update the password entry
        password.site_name = site_name
        password.site_url = site_url
        password.site_password = bcrypt.generate_password_hash(site_password).decode('utf-8')
        db.session.commit()
        
        flash('Password updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_password.html', password=password)

# View Password Route
@main.route('/view_password/<int:id>')
@login_required
def view_password(id):
    password = Password.query.get_or_404(id)
    
    # Ensure the password belongs to the current user
    if password.user_id != current_user.id:
        flash('Access denied. You cannot view this password.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('view_password.html', password=password)

# Delete Password Route
@main.route('/delete_password/<int:id>', methods=['POST'])
@login_required
def delete_password(id):
    password = Password.query.get_or_404(id)
    
    # Ensure the password belongs to the current user
    if password.user_id != current_user.id:
        flash('Access denied. You cannot delete this password.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Delete the password entry
    try:
        db.session.delete(password)
        db.session.commit()
        flash('Password deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting password: {str(e)}', 'danger')
        db.session.rollback()
    
    return redirect(url_for('main.dashboard'))

# Share Password Route
@main.route('/share_password/<int:password_id>', methods=['GET', 'POST'])
@login_required
def share_password(password_id):
    password = Password.query.get_or_404(password_id)
    
    if password.user_id != current_user.id:
        flash('Access denied. You cannot share this password.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        expiry_hours = int(request.form.get('expiry_hours', 24))  # Default: 24 hours
        expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)
        token = generate_token()
        
        shared_password = SharedPassword(
            token=token,
            expiry_time=expiry_time,
            password_id=password.id,
            user_id=current_user.id
            
        )
        
        try:
            db.session.add(shared_password)
            db.session.commit()
            shareable_link = f"{request.host_url}view_shared_password/{token}"
            flash(f'Password shared successfully! Share this link: {shareable_link}', 'success')
            return redirect(url_for('main.dashboard'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred while sharing the password.', 'danger')
            return redirect(url_for('main.share_password', password_id=password_id))
    
    return render_template('share_password.html', password=password)

# View Shared Password Route
@main.route('/view_shared_password/<token>')
def view_shared_password(token):
    shared_password = SharedPassword.query.filter_by(token=token).first()
    
    if not shared_password:
        flash('Invalid or expired link.', 'danger')
        return redirect(url_for('main.home'))
    
    if shared_password.is_used:
        flash('This link has already been used.', 'danger')
        return redirect(url_for('main.home'))
    
    if datetime.utcnow() > shared_password.expiry_time:
        flash('This link has expired.', 'danger')
        return redirect(url_for('main.home'))
    
    # Mark the link as used
    shared_password.is_used = True
    db.session.commit()
    
    # Display the password
    password = shared_password.password
    return render_template('view_shared_password.html', password=password)