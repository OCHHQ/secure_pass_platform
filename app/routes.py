# backend/app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, abort, send_file, current_app, g
from datetime import datetime, timedelta
from app.api.v1.auth.utils import token_required
import secrets
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import re
from functools import wraps
import pyotp
import zxcvbn
import os
import json
from io import BytesIO
from cryptography.fernet import Fernet
from .models import User, Password, SharedPassword, db, PasswordHistory
from . import bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.forms import AddPasswordForm, SharePasswordForm


# Create the main blueprint
main = Blueprint('main', __name__)

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Generate a unique token for sharing
def generate_token():
    return secrets.token_urlsafe(32)

# Password validation
def is_strong_password(password):
    """Check if password meets security requirements"""
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, "Password is strong"


# Helper function to check password ownership
def check_password_ownership(password_id, user_id):
    password = Password.query.get_or_404(password_id)
    if password.user_id != user_id:
        abort(403)
    return password

# Function to encrypt passwords for export
def encrypt_passwords_for_export(passwords):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    passwords_str = json.dumps([password.to_dict() for password in passwords])
    encrypted_data = cipher_suite.encrypt(passwords_str.encode())
    encrypted_file = BytesIO(encrypted_data)
    return encrypted_file

# Function to decrypt passwords from import
def decrypt_passwords_from_import(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    passwords = json.loads(decrypted_data.decode())
    return passwords


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
        
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists.', 'danger')
            return redirect(url_for('main.register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
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


@main.route('/enable_2fa')
@token_required
def enable_2fa():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        request.user.email,  # Access user from request context
        issuer_name="Secure Password Manager"
    )
    return render_template('enable_2fa.html', 
                         secret=secret, 
                         qr_code=provisioning_uri)

@main.route('/verify_2fa', methods=['POST'])
@token_required
def verify_2fa():
    totp = pyotp.TOTP(request.user.totp_secret)  # Access user from request context
    if totp.verify(request.form.get('totp_code')):
        flash('2FA verification successful!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Invalid 2FA code.', 'danger')
        return redirect(url_for('main.enable_2fa'))


# Dashboard Route
@main.route('/dashboard')
@token_required
def dashboard():
    try:
        user_id = request.user.id  # Access user from request context
        page = request.args.get('page', 1, type=int)
        per_page = 10

        passwords_query = Password.query.filter_by(user_id=user_id)
        paginated_passwords = passwords_query.order_by(Password.last_modified.desc())\
            .paginate(page=page, per_page=per_page)
        
        total_passwords = passwords_query.count()
        weak_passwords = passwords_query.filter_by(strength='weak').count()
        
        recent_activities = PasswordHistory.query.filter_by(user_id=user_id)\
            .order_by(PasswordHistory.timestamp.desc())\
            .limit(5).all()

        shared_passwords = SharedPassword.query.join(Password)\
            .filter(Password.user_id == user_id)\
            .order_by(SharedPassword.expiry_time.desc()).all()

        passwords = paginated_passwords.items
        for password in passwords:
            password.age_warning = False
            if password.last_modified:
                password.age_warning = (datetime.utcnow() - password.last_modified).days > 90

        return render_template(
            'dashboard.html',
            passwords=passwords,
            shared_passwords=shared_passwords,
            page=page,
            total_pages=paginated_passwords.pages,
            datetime=datetime,
            total_passwords=total_passwords,
            weak_passwords=weak_passwords,
            recent_activities=recent_activities
        )

    except Exception as e:
        print(f"Error in dashboard route: {str(e)}")
        flash('An error occurred while loading the dashboard.', 'danger')
        return redirect(url_for('main.home'))

# Logout Route
@main.route('/logout')
@main.route('/logout')
@token_required
def logout():
    # Since we're using token auth, we just need to redirect
    # The frontend should handle clearing the token
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

@main.route('/export_passwords')
@token_required
def export_passwords():
    user_id = g.user.id
    passwords = Password.query.filter_by(user_id=user_id).all()
    encrypted_data = encrypt_passwords_for_export(passwords)
    return send_file(
        encrypted_data,
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='passwords_backup.enc'
    )

@main.route('/import_passwords', methods=['GET', 'POST'])
@token_required
def import_passwords():
    user_id = g.user.id
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.enc'):
            passwords = decrypt_passwords_from_import(file.read())
            for password in passwords:
                new_password = Password(
                    user_id=user_id,
                    site_name=password['site_name'],
                    site_url=password['site_url'],
                    site_password=password['site_password']
                )
                db.session.add(new_password)
            db.session.commit()
            flash('Passwords imported successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid file format.', 'danger')
    return render_template('import_passwords.html')

# add_password Route
# add_password Route
@main.route('/add_password', methods=['GET', 'POST'])
@token_required  # Change login_required to token_required for consistency
@limiter.limit("20/hour")
def add_password():
    form = AddPasswordForm()
    
    if request.method == 'POST':
        print("Form submitted with data:", {
            'site_name': request.form.get('site_name'),
            'site_url': request.form.get('site_url'),
            'password_length': len(request.form.get('site_password', ''))
        })
        print("Form validation errors:", form.errors)
    
    if form.validate_on_submit():
        try:
            site_name = form.site_name.data.strip()
            site_url = form.site_url.data.strip() if form.site_url.data else ''
            site_password = form.site_password.data

            # Check for duplicate entries
            existing_password = Password.query.filter_by(
                user_id=request.user.id,  # Changed from current_user to request.user
                site_name=site_name
            ).first()
            
            if existing_password:
                flash('A password for this site already exists.', 'danger')
                return render_template('add_password.html', form=form)

            # Create new password entry
            hashed_password = bcrypt.generate_password_hash(site_password).decode('utf-8')
            
            strength_result = zxcvbn.zxcvbn(site_password)
            strength = 'strong' if strength_result['score'] >= 3 else 'weak'
            
            new_password = Password(
                user_id=request.user.id,  # Changed from current_user to request.user
                site_name=site_name,
                site_url=site_url,
                site_password=hashed_password,
                strength=strength,
                last_modified=datetime.utcnow()
            )

            # Create history entry
            history = PasswordHistory(
                user_id=request.user.id,  # Changed from current_user to request.user
                action='create',
                site_name=site_name,
                timestamp=datetime.utcnow()
            )

            db.session.add(new_password)
            db.session.add(history)
            db.session.commit()

            flash('Password added successfully!', 'success')
            return redirect(url_for('main.dashboard'))

        except Exception as e:
            print(f"Error adding password: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            db.session.rollback()
            flash('An error occurred while adding the password.', 'danger')
            return render_template('add_password.html', form=form)
    
    return render_template('add_password.html', form=form)

# Edit Password Route
@main.route('/edit_password/<int:id>', methods=['GET', 'POST'])
@token_required
def edit_password(id):
    try:
        user_id = request.user.id  # Access user from request context
        password = check_password_ownership(id, user_id)
        
        if request.method == 'POST':
            site_name = request.form.get('site_name').strip()
            site_url = request.form.get('site_url').strip()
            site_password = request.form.get('site_password')
            
            if not site_name or not site_password:
                flash('Site name and password are required.', 'danger')
                return redirect(url_for('main.edit_password', id=id))
            
            is_strong, message = is_strong_password(site_password)
            if not is_strong:
                flash(message, 'warning')
                return redirect(url_for('main.edit_password', id=id))
            
            password.site_name = site_name
            password.site_url = site_url
            password.site_password = bcrypt.generate_password_hash(site_password).decode('utf-8')
            password.strength = 'strong' if is_strong else 'weak'
            password.last_modified = datetime.utcnow()
            
            history = PasswordHistory(
                user_id=user_id,
                action='edit',
                site_name=site_name,
                timestamp=datetime.utcnow()
            )
            
            db.session.add(history)
            db.session.commit()
            
            flash('Password updated successfully!', 'success')
            return redirect(url_for('main.dashboard'))
            
    except Exception as e:
        flash('An error occurred while updating the password.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('edit_password.html', password=password)

# View Password Route
@main.route('/view_password/<int:id>')
@token_required
def view_password(id):
    try:
        user_id = g.user.id
        password = check_password_ownership(id, user_id)
        
        # Record view history
        history = PasswordHistory(
            user_id=user_id,
            action='view',
            site_name=password.site_name,
            timestamp=datetime.utcnow()
        )
        db.session.add(history)
        db.session.commit()
        
        return render_template('view_password.html', password=password)
    except Exception as e:
        flash('An error occurred while viewing the password.', 'danger')
        return redirect(url_for('main.dashboard'))


# Delete Password Route
@main.route('/delete_password/<int:id>', methods=['POST'])
@token_required
def delete_password(id):
    try:
        user_id = g.user.id
        password = Password.query.get_or_404(id)
        
        if password.user_id != user_id:
            flash('Access denied. You cannot delete this password.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        SharedPassword.query.filter_by(password_id=id).delete()
        db.session.delete(password)
        db.session.commit()
        
        flash('Password deleted successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    
    except Exception as e:
        flash(f'Error deleting password: {str(e)}', 'danger')
        db.session.rollback()
        return redirect(url_for('main.dashboard'))

# Share Password Route
@main.route('/share_password/<int:password_id>', methods=['GET', 'POST'])
@token_required
def share_password(password_id):
    form = SharePasswordForm()
    try:
        user_id = g.user.id
        password = check_password_ownership(password_id, user_id)
        if not password:
            flash('Password not found or access denied.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        if form.validate_on_submit():
            expiry_hours = form.expiry_hours.data
            expiry_time = datetime.utcnow() + timedelta(hours=expiry_hours)
            token = generate_token()
            
            active_shares = SharedPassword.query.filter_by(
                password_id=password.id,
                is_used=False
            ).filter(SharedPassword.expiry_time > datetime.utcnow()).count()
            
            if active_shares >= 5:
                flash('Maximum number of active shares reached.', 'warning')
                return redirect(url_for('main.share_password', password_id=password_id))
            
            shared_password = SharedPassword(
                token=token,
                expiry_time=expiry_time,
                password_id=password.id,
                user_id=user_id,
                is_used=False
            )
            
            history = PasswordHistory(
                user_id=user_id,
                action='share',
                site_name=password.site_name,
                timestamp=datetime.utcnow()
            )
            
            db.session.add(shared_password)
            db.session.add(history)
            db.session.commit()
            
            shareable_link = url_for('main.view_shared_password', 
                                   token=token, 
                                   _external=True)
            
            return render_template('share_password_success.html', 
                                 shareable_link=shareable_link,
                                 expiry_hours=expiry_hours)
            
    except Exception as e:
        current_app.logger.error(f"Error in share_password route: {str(e)}")
        flash('An unexpected error occurred. Please try again later.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    return render_template('share_password.html', 
                         form=form, 
                         password=password)
# View Shared Password Route
@main.route('/view_shared_password/<token>')
def view_shared_password(token):
    try:
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
    except Exception as e:
        flash('An error occurred while viewing the shared password.', 'danger')
        return redirect(url_for('main.home'))