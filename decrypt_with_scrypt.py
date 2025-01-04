import hashlib
import binascii

# Encrypted password format:
# scrypt:<iterations>:<block_size>:<parallelism>$<salt>$<key>
encrypted_password = "scrypt:32768:8:1$nszsfmWOy4w2Mqtu$e0b4e708ebd87b7a44d0cf00a10e9bab8a48a60396bc85eb18be772d702ba108670dd0349fda268070a1bdb6a13f2c0a6739cb3d89a6ddd4ae133bae1f6a0fb3"

def decrypt_with_scrypt(encrypted_password, master_password):
    try:
        print(f"Encrypted Password: {encrypted_password}")
        
        # Extract scrypt parameters and stored key
        parts = encrypted_password.split('$')
        if len(parts) != 3:
            raise ValueError("Invalid encrypted password format")
        
        scrypt_params = parts[0]  # Example: scrypt:32768:8:1
        salt = parts[1]           # Example: nszsfmWOy4w2Mqtu
        encrypted_key = parts[2]  # Example: e0b4...

        print(f"scrypt_params: {scrypt_params}")
        print(f"salt: {salt}")
        print(f"encrypted_key: {encrypted_key}")

        # Parse scrypt parameters
        _, iterations, block_size, parallelism = scrypt_params.split(':')
        iterations = min(int(iterations), 16384)  # Adjust to system capacity
        block_size = min(int(block_size), 4)      # Reduce block size
        parallelism = min(int(parallelism), 1)    # Limit parallelism

        # Decode salt (Base64) and encrypted key (Hex)
        salt = binascii.a2b_base64(salt)  # Convert Base64-encoded salt to bytes
        stored_key = binascii.unhexlify(encrypted_key)  # Convert Hex-encoded key to bytes

        # Use scrypt to derive the key
        derived_key = hashlib.scrypt(
            password=master_password.encode(),
            salt=salt,
            n=iterations,  # Adjusted CPU/memory cost factor
            r=block_size,  # Reduced block size
            p=parallelism,  # Single-threaded decryption
            dklen=len(stored_key)  # Length of derived key
        )

        # Compare derived key to stored key
        if derived_key == stored_key:
            print("Password matches!")
        else:
            print("Password does not match.")

    except Exception as e:
        print("Error during scrypt decryption:", e)

# Test the function with the correct password
decrypt_with_scrypt(encrypted_password, 'correct_master_password')
