from cryptography.fernet import Fernet
import sys
import os

ENV_SECRET = os.getenv("ENV_SECRET") # Get the secret key from environment variable

def generate_key():
    """Generate a new key for encryption"""
    key = Fernet.generate_key()
    print(f"Generated Key: {key.decode()}")
    return key

def encrypt_file(input_file, output_file, key):
    """Encrypt a file using Fernet symmetric encryption"""
    cipher_suite = Fernet(key)
    with open(input_file, 'rb') as file:
        encrypted_data = cipher_suite.encrypt(file.read())
    with open(output_file, 'wb') as file:
        file.write(encrypted_data)
    print(f"Encrypted: {output_file}")

def decrypt_file(input_file, output_file, key):
    """Decrypt a file using Fernet symmetric encryption"""
    cipher_suite = Fernet(key)
    with open(input_file, 'rb') as file:
        decrypted_data = cipher_suite.decrypt(file.read())
    with open(output_file, 'wb') as file:
        file.write(decrypted_data)
    print(f"Decrypted: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "generate":
        generate_key()
        sys.exit(0)
    if len(sys.argv) != 4:
        print("Usage: python encrypt_decrypt_env.py <encrypt/decrypt> <input_file> <output_file>")
        sys.exit(1)

    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if not ENV_SECRET:
        print("ENV_SECRET environment variable not set")
        sys.exit(1)

    if action == "encrypt":
        encrypt_file(input_file, output_file, ENV_SECRET)
    elif action == "decrypt":
        decrypt_file(input_file, output_file, ENV_SECRET)
    else:
        print("Invalid action. Use 'encrypt' or 'decrypt'.")
        sys.exit(1)