from cryptography.fernet import Fernet
from app import create_app, db
from app.models import User

app = create_app()

def test_decryption():
    print("Script started")

    # Replace with your secret key (make sure it's correct)
    secret_key = "ODoxV1FUvvQ4dnxAW0QlgnW7Vrhe5dgEysGVrX_dtGk=".encode()

    print("Secret key loaded")

    with app.app_context():
        print("App context established")

        # Retrieve a user from the database
        user = User.query.first()
        print(f"User found: {user}")

        if user:
            print("User found in the database")

            # Directly use the encrypted password from the database
            encrypted_password = user.encrypted_password.encode()  # Ensure it's in bytes
            print(f"Encrypted password: {encrypted_password}")

            try:
                # Decrypt the password
                f = Fernet(secret_key)
                decrypted_password = f.decrypt(encrypted_password).decode()

                print("Decrypted password:", decrypted_password)
            except Exception as e:
                print("Decryption error:", str(e))
                import traceback
                traceback.print_exc()
        else:
            print("No users found in the database.")

    print("Script finished")

test_decryption()
