import bcrypt

class Hash:
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Parameters:
            password (str): The plain text password to hash.
            
        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password.
        
        Parameters:
            password (str): The plain text password to verify.
            hashed_password (str): The hashed password to compare against.
            
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
