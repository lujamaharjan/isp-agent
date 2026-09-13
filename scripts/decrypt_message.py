from cryptography.fernet import Fernet


STATIC_KEY = b"4TOWSVrsnbwThSvHdMNnQAKfbPbRa3vnKuvH8vZtQa0="
cipher_suite = Fernet(STATIC_KEY)

encrypted_message = b"gAAAAABqSY7b_RZpmffmha-ON4EBwsBdro3l8HsT21UcCx2IpcA9zAdl9SNI0XAMZzkzTpF6FaC8iVSPyMsUS25mEmHnzEJGCZY7YUmLzypfAqlsrXo-h56IUcRbvAuVDensmZT-ijR3"

try:
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode("utf-8")
    print(f"Decrypted Message: {decrypted_message}")
except Exception as error:
    print(f"Decryption failed: {error}")