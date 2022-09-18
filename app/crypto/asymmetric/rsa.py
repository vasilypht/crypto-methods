# The module contains the implementation of the RSA asymmetric encryption algorithm
from dataclasses import dataclass
from secrets import SystemRandom

from app.crypto.mathlib import (
    ext_gcd,
    modinv,
    fpow
)
from app.crypto.utils import gen_prime
from app.crypto.common import EncProc


class RSA:

    @dataclass(frozen=True)
    class PrivateKey:
        d: int
        n: int

    @dataclass(frozen=True)
    class PublicKey:
        e: int
        n: int

    def __init__(self, private_key: PrivateKey, public_key: PublicKey) -> None:
        """
        Implementation of the asymmetric RSA encryption algorithm.

        private_key
            Private key of type RSA.PrivateKey, which contains the number D and the modulus N.
        public_key
            Public key of type RSA.PublicKey, which contains the number E and the modulus N.
        """
        if not (isinstance(private_key, RSA.PrivateKey) and isinstance(public_key, RSA.PublicKey)):
            raise TypeError("Arguments must be of type RSA.PrivateKey and RSA.PublicKey.")

        self._private_key = private_key
        self._public_key = public_key

    @property
    def num_bytes_to_encrypt(self):
        """The maximum number of bytes that can be read from the file to encrypt."""
        return (self._public_key.n.bit_length() >> 3) - 1

    @property
    def num_bytes_to_decrypt(self):
        """The maximum number of bytes that can be read from the file to be decrypted."""
        return self._private_key.n.bit_length() >> 3

    def encrypt(self, data: int or bytes) -> int or bytes:
        """
        Method for encrypting data.

        data
            Data to encrypt.
            - If the input data is of type int, then the result of the method will be a number.
            - If the input data is of type bytes, then the result of the method will be bytes,
            and the number of bytes will be equal to the number of module bytes in the order of little endian
        """
        match data:
            case int():
                return fpow(data, self._public_key.e, self._public_key.n)

            case bytes():
                data = int.from_bytes(data, "little")
                encrypted_data = fpow(data, self._public_key.e, self._public_key.n)
                return encrypted_data.to_bytes(self._public_key.n.bit_length() >> 3, "little")

            case _:
                raise TypeError("Possible types: int, bytes.")

    def decrypt(self, data: int or bytes) -> int or bytes:
        """
        Method for decrypting data

        data
            Data to decrypt.
            - If the input data is of type int, then the result of the method will be a number.
            - If the input data is of type bytes, then the result of the method will be bytes, and
            the number of bytes will be equal to the number of bytes of the module minus 1 - that
            is, the maximum number of bytes that can be used for encryption with this module in
            the order of little endian.
        """
        match data:
            case int():
                return fpow(data, self._private_key.d, self._private_key.n)

            case bytes():
                data = int.from_bytes(data, "little")
                decrypted_data = fpow(data, self._private_key.d, self._private_key.n)
                return decrypted_data.to_bytes((self._private_key.n.bit_length() >> 3) - 1, "little")

            case _:
                raise TypeError("Possible types: int, bytes.")

    def make(self, data: int or bytes, enc_proc: EncProc) -> int or bytes:
        """
        Method for encrypting and decrypting data.

        data
            Data to decrypt or encrypt.
            - (Encrypt) If the input data is of type int, then the result of the method will be a number.
            - (Encrypt) If the input data is of type bytes, then the result of the method will be bytes,
            and the number of bytes will be equal to the number of module bytes in the order of little endian
            - (Decrypt) If the input data is of type int, then the result of the method will be a number.
            - (Decrypt) If the input data is of type bytes, then the result of the method will be bytes, and
            the number of bytes will be equal to the number of bytes of the module minus 1 - that
            is, the maximum number of bytes that can be used for encryption with this module in
            the order of little endian.
            Encryption process. For the encryption process, use the EncProc enumeration.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(data)

            case EncProc.DECRYPT:
                return self.decrypt(data)

            case _:
                raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")

    @staticmethod
    def gen_keys(key_size: int = 1024, p: int = None, q: int = None) -> tuple[PrivateKey, PublicKey]:
        """
        Method for generating private and public keys.

        If P and Q are not specified at the same time, they will be generated with the specified
        size. If P and Q are specified, then the key size parameter is ignored. When manually
        setting the parameters P and Q, you need to make sure that P and Q are prime numbers.

        key_size
            Number of bits to generate prime p and q.
        p
            Prime number to generate private and public keys.
        q
            Prime number to generate private and public keys.
        """
        if not (p and q):
            p = gen_prime(key_size)
            q = gen_prime(key_size)

        n = p * q

        phi = (p-1) * (q-1)
        sysrand = SystemRandom()
        while True:
            e = sysrand.randrange(2, phi)
            if ext_gcd(e, phi).gcd == 1:
                break

        d = modinv(e, phi)

        return RSA.PrivateKey(d, n), RSA.PublicKey(e, n)
