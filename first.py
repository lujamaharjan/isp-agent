from cryptography.fernet import Fernet

# Use the same static key as before
STATIC_KEY = b'4TOWSVrsnbwThSvHdMNnQAKfbPbRa3vnKuvH8vZtQa0='
cipher_suite = Fernet(STATIC_KEY)

# Example encrypted message
encrypted_message = b'gAAAAABqSY7b_RZpmffmha-ON4EBwsBdro3l8HsT21UcCx2IpcA9zAdlS9NI0XAMZzkzTpF6FaC8iVSPyMsUS25mEmHnzEJGCZY7YUmLzypfAqlsrXo-h56IUcRbvAuVDensmZT-ijR3'
# Decrypt the message
try:
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
    print(f"Decrypted Message: {decrypted_message}")
except Exception as e:
    print(f"Decryption failed: {e}")