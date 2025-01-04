from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
from cryptography.hazmat.primitives import padding

# Derive the key using PBKDF2-HMAC
def derive_key(master_password: str, salt: bytes = None) -> tuple:
    if salt is None:
        salt = os.urandom(16)  # Random salt for each password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # Corrected this line
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(master_password.encode())
    return key, salt

# Encrypt the password using AES-CBC
from typing import Tuple

def encrypt_password(password: str, master_password: str) -> Tuple[bytes, bytes]:
    salt = os.urandom(16)
    key, _ = derive_key(master_password, salt)
    
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()
    
    encrypted_password = iv + encryptor.update(padded_data) + encryptor.finalize()
    return encrypted_password, salt

# Decrypt the password using AES-CBC
def decrypt_password(encrypted_password: bytes, master_password: str, salt: bytes) -> str:
    key, _ = derive_key(master_password, salt)
    
    # Extract IV and ciphertext
    iv = encrypted_password[:16]
    ciphertext = encrypted_password[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    padding_length = padded_data[-1]
    return padded_data[:-padding_length].decode()
