import unittest
from app.services import encrypt_password, decrypt_password

class TestEncryptionDecryption(unittest.TestCase):
    def setUp(self):
        self.master_password = "master_password"
        self.password = "This is a secret password"

    def test_encrypt_decrypt(self):
        encrypted_password, salt = encrypt_password(self.password, self.master_password)
        decrypted_password = decrypt_password(encrypted_password, self.master_password, salt)
        self.assertEqual(self.password, decrypted_password)

if __name__ == '__main__':
    unittest.main()