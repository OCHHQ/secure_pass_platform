from typing import Self
import unittest
from app import create_app, db
from app.models import User, Password
from app.services import encrypt_password, decrypt_password
from flask_login import current_user

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SECRET_KEY': 'test-secret-key'
        })
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def signup(self, username, password):
        return self.client.post('/signup', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def test_encrypt_decrypt_password(self):
        """Test the encryption and decryption of passwords"""
        password = 'mysecretpassword'
        master_password = 'masterpass'
        
        try:
            # Test encryption
            encrypted_password, salt = encrypt_password(password, master_password)
            self.assertIsNotNone(encrypted_password)
            self.assertIsNotNone(salt)
            self.assertTrue(len(encrypted_password) >= 16)
            
            # Test decryption
            decrypted_password = decrypt_password(encrypted_password, master_password, salt)
            self.assertEqual(decrypted_password, password)
            
            # Test with different lengths
            test_cases = ['a', 'ab', 'abc', 'a' * 16, 'a' * 32]
            for test_password in test_cases:
                encrypted, salt = encrypt_password(test_password, master_password)
                decrypted = decrypt_password(encrypted, master_password, salt)
                self.assertEqual(decrypted, test_password)
                
        except Exception as e:
            self.fail(f"Encryption/decryption failed with error: {str(e)}")

    def test_signup_login(self):
        """Test user registration and login functionality"""
        # Test successful signup
        response = self.signup('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        
        # Test duplicate username
        response = self.signup('testuser', 'anotherpassword')
        self.assertIn(b'Username already exists', response.data)
        
        # Test successful login
        response = self.login('testuser', 'testpassword')
        self.assertEqual(response.status_code, 200)
        # Check for welcome message instead of login successful
        self.assertIn(b'Welcome back, testuser', response.data)
        
        # Test incorrect password
        response = self.login('testuser', 'wrongpassword')
        self.assertIn(b'Login failed. Check username and/or password.', response.data)
        
        # Test non-existent user
        response = self.login('nonexistent', 'testpassword')
        self.assertIn(b'Login failed. Check username and/or password.', response.data)

    def test_logout(self):
        """Test user logout functionality"""
        self.signup('testuser', 'testpassword')
        self.login('testuser', 'testpassword')
        
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)

    def test_add_password(self):
        """Test password addition functionality"""
        self.signup('testuser', 'testpassword')
        self.login('testuser', 'testpassword')
        
        # Test successful password addition
        response = self.client.post('/add_password', data={
            'title': 'Test Password',
            'password': 'mysecretpassword',
            'master_password': 'mystrongpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password added successfully', response.data)
        
        # Verify password was added to database
        password = Password.query.filter_by(title='Test Password').first()
        self.assertIsNotNone(password)
        
        # Test duplicate title (if your app prevents this)
        response = self.client.post('/add_password', data={
            'title': 'Test Password',
            'password': 'differentpassword',
            'master_password': 'mystrongpassword'
        }, follow_redirects=True)
        
        # Test missing required fields
        response = self.client.post('/add_password', data={
            'title': 'Test Password'
        }, follow_redirects=True)
        self.assertNotEqual(response.status_code, 500)

    def test_view_password(self):
        """Test password viewing functionality"""
        # Setup
        self.signup('testuser', 'testpassword')
        self.login('testuser', 'testpassword')
        
        # Add a password
        self.client.post('/add_password', data={
            'title': 'Test Password',
            'password': 'mysecretpassword',
            'master_password': 'mystrongpassword'
        })
        
        password = Password.query.filter_by(title='Test Password').first()
        
        # Test viewing with correct master password
        response = self.client.post(f'/view_password/{password.id}', data={
            'master_password': 'mystrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'mysecretpassword', response.data)
        
        # Test viewing with incorrect master password
        response = self.client.post(f'/view_password/{password.id}', data={
            'master_password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Failed to decrypt the password. Ensure your master password is correct.', response.data)
        
        # Test viewing non-existent password
        response = self.client.get('/view_password/999999', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_delete_password(self):
        """Test password deletion functionality"""
        self.signup('testuser', 'testpassword')
        self.login('testuser', 'testpassword')
        
        # Add a password
        self.client.post('/add_password', data={
            'title': 'Test Password',
            'password': 'mysecretpassword',
            'master_password': 'mystrongpassword'
        })
        
        password = Password.query.filter_by(title='Test Password').first()
        
        # Test successful deletion
        response = self.client.post(f'/delete_password/{password.id}', 
                                  follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Password deleted successfully', response.data)
        deleted_password = Password.query.filter_by(title='Test Password').first()
        self.assertIsNone(deleted_password)
        
        # Test deleting non-existent password
        response = self.client.post('/delete_password/999999', 
                                  follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_access_control(self):
        """Test access control and authorization"""
        # Create two users
        self.signup('user1', 'password1')
        self.login('user1', 'password1')
        
        # Add a password
        self.client.post('/add_password', data={
            'title': 'User1 Password',
            'password': 'secret1',
            'master_password': 'master1'
        })
        
        password = Password.query.filter_by(title='User1 Password').first()
        
        # Login as user2 and try to access user1's password
        self.signup('user2', 'password2')
        self.login('user2', 'password2')
        
        # Try to view password (directly checking status code before redirect)
        response = self.client.get(f'/view_password/{password.id}')
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        response = self.client.get(f'/view_password/{password.id}', follow_redirects=True)
        self.assertIn(b'Access denied. You do not own this password.', response.data)
        
        # Try to delete password
        response = self.client.post(f'/delete_password/{password.id}')
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        response = self.client.post(f'/delete_password/{password.id}', follow_redirects=True)
        self.assertIn(b'Access denied. You cannot delete this password.', response.data)

if __name__ == '__main__':
    unittest.main()