import keyring
import os
import pbkdf2
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import base64

class ToooMailCrypt:
    """
    This class contains the methods used to store
    an email's password securely from the system
    keyring in encrypted form and to decrypt an
    email's password once retrieved.

    Example usage:

    >>> CryptAPI = ToooMailCrypt()
    >>> CryptAPI.save_credentials("sample@email.com", "EmailPassword", "ToooMailPassword")
    >>> encrypted = CryptAPI.get_password("sample@email.com")
    >>> print(encrypted)
    'tLyqT8ChzgrmjMA51A=='
    >>> decrypted = CryptAPI.decrypt("sample@email.com", "ToooMailPassword")
    >>>print(decrypted)
    'EmailPassword'
    """    


    BACKEND = default_backend()

    def derive_key(self,password, size: int = 256):
        """
        Derives a size bits key deterministically for use in
        the self.encrypt() function as an AES key
        """
        
        return pbkdf2.PBKDF2(password, salt='').read(size // 8)

    def encrypt(self, password: str, email: str, tooomail_password: str):
        """
        Encrypts the email's password using the email and the master password
        as parameters for the cipher. This operation can be reversed in the
        self.decrypt() function giving the master password and the desired email
        as parameters to the function.
        """
        
        iv = bytes(sha256(email.encode()).hexdigest(), "u8")[0:16]
        cipher = Cipher(algorithms.AES(self.derive_key(tooomail_password)), modes.CTR(iv), backend=self.BACKEND)
        encryptor = cipher.encryptor()
        pwd = encryptor.update(bytes(password, "u8")) + encryptor.finalize()
        return base64.b64encode(pwd).decode()


    def get_password(self, email: str):
        """
        Retrieves the password associated with the given email
        from the system keyring if present, None otherwhise.
        """
        
        return keyring.get_password("ToooMail", email)

    def decrypt(self, email: str, tooomail_password: str):
        """"
        Decrypts the email's password using the email and the master password
        as parameters for the cipher. This operation is the inverse of what
        happens inside the self.encrypt() function.
        """"
        
        iv = bytes(sha256(email.encode()).hexdigest(), "u8")[0:16]
        cipher = Cipher(algorithms.AES(self.derive_key(tooomail_password)), modes.CTR(iv), backend=self.BACKEND)
        decryptor = cipher.decryptor()
        pwd = decryptor.update(base64.b64decode(self.get_password(email).encode())) + decryptor.finalize()
        return pwd.decode()
    
    def save_credentials(self, email: str, email_password: str, tooomail_password: str):
        """
        Saves a given email-password couple in the system keyring. The email's
        password is encrypted before being stored thanks to the self.encrypt()
        function and the email and the master password as parameters.
        """
            keyring.set_password("ToooMail", email, self.encrypt(email_password, email, tooomail_password))

# Sample usage of the CryptoAPI
# CryptAPI = ToooMailCrypt()
# CryptAPI.save_credentials("sample@email.com", "EmailPassword", "ToooMailPassword")
# encrypted = CryptAPI.get_password("sample@email.com")
# print(encrypted) # output: 'tLyqT8ChzgrmjMA51A=='
# decrypted = CryptAPI.decrypt("sample@email.com", "ToooMailPassword")
# print(decrypted) # output: 'EmailPassword'
