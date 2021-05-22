from cryptography.fernet import Fernet
from twopassword.settings import FERNET_SECRET_KEY


class Encryptor:
    """A simple class for encrypting & decrypting strings."""

    def __init__(self, key=None):
        """Initializes the Encryptor class.

        Args:
            key (str, optional): The key to initialize Fernet with.
        """
        if not key:
            key = FERNET_SECRET_KEY

        self.fernet = Fernet(key)

    def encrypt(self, msg):
        """Encrypts a string & returns it.

        Args:
            msg (str): The string to encrypt.

        Returns:
            str: the encrypted string.
        """
        return self.fernet.encrypt(msg.encode()).decode('utf-8')

    def decrypt(self, msg):
        """Decrypts a string & returns it.

        Args:
            msg (str): The encrypted string to decrypt.

        Returns:
            str: the decrypted string.
        """
        return self.fernet.decrypt(msg.encode()).decode('utf-8')
