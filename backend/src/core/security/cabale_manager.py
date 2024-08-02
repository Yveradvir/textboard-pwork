import hashlib
import base64
import json
import datetime as d

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

from typing import Dict, Any

from src.core.const import _genv
from src.core.security.models import CabaleSettings

class CabaleTokenManager:
    """
    A class to handle the generation and verification of Cabale tokens.
    """

    def __init__(self, settings: CabaleSettings) -> None:
        """
        Initialize the CabaleTokenManager with settings.

        Parameters:
            settings (CabaleSettings): An instance of CabaleSettings containing the encryption key.
        """
        self.settings = settings
    
    def _iat(self) -> float:
        """Returns POSIX time"""
        return d.datetime.now(d.timezone.utc).timestamp()    
    
    def _generate_key(self) -> bytes:
        """
        Generate a 32-byte key from the secret key.

        Returns:
            bytes: A 32-byte key derived from the secret key.
        """
        hasher = hashlib.sha256()
        hasher.update(self.settings.key.encode())
        return hasher.digest()

    def generate_cabale_token(
        self, data: Dict[str, Any], uuid: str, iv: bytes
    ) -> str:
        """
        Generate a Cabale token.

        Parameters:
            data (Dict[str, Any]): A dictionary containing the data to be encoded in the token.
            uuid ( str(uuid4()) ): A unique identifier to be included in the token.
            iv (bytes): A 16-byte initialization vector used for AES encryption.

        Returns:
            str: The generated Cabale token in the format `uuid:@:base64(encrypted_data)`.
        """
        key = self._generate_key()
        
        data['id'] = uuid
        data['iat'] = self._iat()
        
        json_data = json.dumps(data)
        json_data = json_data.encode()
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        
        padded_data = padder.update(json_data) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        
        return f"{str(uuid)}:@:{base64.b64encode(encrypted).decode()}"

    def verify_cabale_token(
        self, cabale_token: str, iv: bytes
    ) -> Dict[str, Any] | None:
        """
        Verify and decode a Cabale token.

        Parameters:
            cabale_token (str): The Cabale token to be verified.
            iv (bytes): The 16-byte initialization vector used for AES decryption.

        Returns:
            Dict[str, Any] | None: The decoded data if the token is valid, otherwise None.
        """
        try:
            key = self._generate_key()

            uuid, encrypted_data = cabale_token.split(":@:")
            encrypted_data = base64.b64decode(encrypted_data)

            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            padder = padding.PKCS7(algorithms.AES.block_size).unpadder()

            padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
            data = padder.update(padded_data) + padder.finalize()

            data_dict = json.loads(data.decode())

            return data_dict
        except Exception as e:
            print(e)
            return {"detail": str(e)}
                
cabale = CabaleTokenManager(
    CabaleSettings(
        key=_genv("SECRET_KEY")
    )
)
