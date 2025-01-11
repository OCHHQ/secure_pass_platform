from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt

def migrate_passwords():
    app = create_app()
    bcrypt = Bcrypt(app)  # Initialize bcrypt

    with app.app_context():
        print("Starting password migration...")
        try:
            users = User.query.all()
            migrated_count = 0
            
            for user in users:
                print(f"Processing user: {user.username}")
                try:
                    # Ensure the password is a string
                    password = user.password
                    if isinstance(password, bytes):
                        password = password.decode('utf-8')  # Convert bytes to string
                    
                    # Check if password is not already hashed with bcrypt
                    if not password.startswith('$2b$'):  # Bcrypt hashes start with $2b$
                        # Hash the password using bcrypt
                        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                        user.password = hashed_password
                        migrated_count += 1
                        print(f"Migrated password for user: {user.username}")
                except Exception as e:
                    print(f"Error processing user {user.username}: {str(e)}")
                    continue
            
            db.session.commit()
            print(f"Successfully migrated {migrated_count} passwords")
            
        except Exception as e:
            print(f"Migration failed: {str(e)}")
            db.session.rollback()

if __name__ == "__main__":
    migrate_passwords()