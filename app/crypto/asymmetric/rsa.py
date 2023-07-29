# The module contains the implementation of the RSA asymmetric encryption algorithm
from secrets import SystemRandom
from dataclasses import dataclass
from math import ceil
from typing import Literal

from app.crypto.mathlib import (
    ext_gcd,
    modinv,
    fpow
)
from app.crypto.utils import gen_prime
from app.crypto.common import EncProc


class RSA:
    @dataclass
    class PublicKey:
        e: int
        n: int

    @dataclass
    class PrivateKey:
        d: int
        n: int

    def __init__(self, private_key: PrivateKey = None, public_key: PublicKey = None) -> None:
        """
        Implementation of the asymmetric RSA encryption algorithm.

        private_key
            Private key of type RSAPrivateKey, which contains the number D and the modulus N.
        public_key
            Public key of type RSAPublicKey, which contains the number E and the modulus N.
        """

        #if not (isinstance(private_key, (RSA.PrivateKey, None)) and isinstance(public_key, RSA.PublicKey)):
        #    raise TypeError("Arguments must be of type RSA.PrivateKey and RSA.PublicKey.")

        #if public_key.n.bit_length() >> 3 <= 512 and private_key.n >> 3 <= 512:
        #    raise ValueError("The module value must be greater than 2 bytes!")

        self._pr_key = private_key
        self._pb_key = public_key

    @property
    def num_bytes_public_module(self):
        return ceil(self._pb_key.n.bit_length() / 8)

    @property
    def num_bytes_private_module(self):
        return ceil(self._pr_key.n.bit_length() / 8)

    def encrypt(self, data: int or bytes, byteorder: Literal["big", "little"] = "big") -> int or bytes:
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
                return fpow(data, self._pb_key.e, self._pb_key.n)

            case bytes():
                data = int.from_bytes(data, byteorder)
                encrypted_data = fpow(data, self._pb_key.e, self._pb_key.n)
                return encrypted_data.to_bytes(self.num_bytes_public_module, byteorder)

            case _:
                raise TypeError("Possible types: int, bytes.")

    def decrypt(self, data: int or bytes, byteorder: Literal["big", "little"] = "big") -> int or bytes:
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
                return fpow(data, self._pr_key.d, self._pr_key.n)

            case bytes():
                data = int.from_bytes(data, byteorder)
                decrypted_data = fpow(data, self._pr_key.d, self._pr_key.n)
                return decrypted_data.to_bytes(self.num_bytes_private_module - 1, byteorder)

            case _:
                raise TypeError("Possible types: int, bytes.")

    def make(self, data: int or bytes, enc_proc: EncProc, byteorder: Literal["big", "little"] = "big") -> int or bytes:
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
                return self.encrypt(data, byteorder)

            case EncProc.DECRYPT:
                return self.decrypt(data, byteorder)

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
