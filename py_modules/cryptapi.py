import keyring
import os
import pbkdf2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256

backend = default_backend()


class ToooMailCrypt:

    def __init__(self, email: str, email_password: str, key_password: str, first_time=True):
        self.email = email
        self.email_password = email_password
        if first_time:
            self.first = True
            self.key_password = key_password
        else:
            self.key_password = self.get_password("ToooMail", sha256(self.email.encode()).hexdigest())

    def generate_aes_key(self, size: int = 256):
        return os.urandom(size // 8)

    def derive_key(self, size: int = 256):
        return pbkdf2.PBKDF2(self.key_password).read(size // 8)

    def encrypt(self):
        iv = bytes(sha256(self.email.encode()).hexdigest(), "u8")[0:16]
        cipher = Cipher(algorithms.AES(self.generate_aes_key(256)), modes.CTR(iv), backend=backend)
        encryptor = cipher.encryptor()
        email = encryptor.update(bytes(self.email, "u8"))
        pwd = encryptor.update(bytes(self.email_password, "u8")) + encryptor.finalize()
        if self.first:
            self.save_password("ToooMail", sha256(self.email.encode()).hexdigest(), self.key_password)
        return email, pwd


    def get_password(self, service: str, username: str):
        return keyring.get_password("ToooMail", username)

    def save_password(self, service: str, username: str, password: str):
            keyring.set_password("ToooMail", username, password)

