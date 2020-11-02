from typing import Union

from argon2 import PasswordHasher, exceptions


class PasswordHandler(PasswordHasher):

    def __init__(self):
        super().__init__(time_cost=10, memory_cost=102400, parallelism=8, hash_len=32, salt_len=32, encoding="utf-8")

    def encrypt_password(self, password: str) -> Union[str, bool]:
        try:
            encryption_result = self.hash(password)
        except exceptions.HashingError:
            encryption_result = "Could not hash password"

        return encryption_result

    def decrypt_password(self, hash: str, password: str) -> Union[str, bool]:
        try:
            decryption_result = self.verify(hash=hash, password=password)
        except exceptions.InvalidHash:
            decryption_result = False, "Invalid hash type"
        except exceptions.VerifyMismatchError:
            decryption_result = False, "Verification mismatch"
        except exceptions.VerificationError:
            decryption_result = False, "Decoding failed"
        except exceptions.Argon2Error:
            decryption_result = False, "Internal library argon2 error occured while decrypting"

        return decryption_result
