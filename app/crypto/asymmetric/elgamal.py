# The module contains the implementation of the Elgamal asymmetric encryption algorithm
from secrets import SystemRandom
from dataclasses import dataclass
from math import ceil
from typing import Literal

from sympy import isprime, primitive_root

from app.crypto.mathlib import (
    fpow,
    ext_gcd,
    modinv
)
from app.crypto.utils import gen_prime
from app.crypto.common import EncProc


class Elgamal:

    @dataclass
    class PrivateKey:
        x: int
        g: int
        p: int

    @dataclass
    class PublicKey:
        y: int
        g: int
        p: int

    @dataclass
    class SessionKey:
        k: int

    @dataclass
    class Ciphertext:
        r: int
        s: int

    def __init__(self, pr_key: PrivateKey = None, pb_key: PublicKey = None) -> None:
        """
        Implementation of the asymmetric Elgamal encryption algorithm.

        private_key
            Private key of type Elgamal.PrivateKey, which contains the number D and the modulus N.
        public_key
            Public key of type Elgamal.PublicKey, which contains the number E and the modulus N.
        """
        #if not (isinstance(private_key, ElgamalPrivateKey) and isinstance(public_key, ElgamalPublicKey)):
        #    raise TypeError("Values must be of type Elgamal.PrivateKey and Elgamal.PublicKey.")

        #if public_key.p.bit_length() <= 512 and private_key.p.bit_length() <= 512:
        #    raise ValueError("The module value must be greater than 2 bytes!")

        self._pr_key = pr_key
        self._pb_key = pb_key
        self._sysrand = SystemRandom()

    @staticmethod
    def gen_keys(n: int = 1024, p: int = None) -> tuple[PrivateKey, PublicKey]:
        """
        Method for generating private and public keys.

        If the P parameter is set, then the function of the Sympy library
        will be used to search for the primitive element, which is quite
        time-consuming for large P. If the P parameter is not set, then it
        will be generated with the specified bit dimension. Moreover, in this
        case, the search for the primitive element will be faster, since it
        will be searched for simply a number of the form p = 2q + 1, where q is prime.

        n
            Number of bits to generate prime p.
        p
            Prime number to generate private and public keys&
        """
        if not p:
            while True:
                p = gen_prime(n)
                q = (p-1) >> 1
                if isprime(q):
                    break

            g = 2
            for i in range(2, p-1):
                if fpow(i, q, p) != 1:
                    g = i
                    break

        else:
            g = primitive_root(p)

        sysrand = SystemRandom()
        x = sysrand.randrange(2, p-1)
        y = fpow(g, x, p)
        return Elgamal.PrivateKey(x, g, p), Elgamal.PublicKey(y, g, p)

    @property
    def num_bytes_private_module(self):
        return ceil(self._pr_key.p.bit_length() / 8)

    @property
    def num_bytes_public_module(self):
        return ceil(self._pb_key.p.bit_length() / 8)

    def _gen_session_key(self) -> SessionKey:
        """Method for generating a session key."""
        while True:
            k = self._sysrand.randrange(2, self._pb_key.p - 1)
            if ext_gcd(k, self._pb_key.p - 1).gcd == 1:
                break

        return Elgamal.SessionKey(k)

    def encrypt(self, data: int or bytes, byteorder: Literal["big", "little"] = "big") -> Ciphertext or bytes:
        """
        Method for encrypting data.

        data
            Data to encrypt.
            - If the input data is of type int, then the result of the method will
            be a Ciphertext object containing two numbers A and B.
            - If the input data is of type bytes, then the result of the method will
            be bytes that contain the number A and the number B, which are connected
            in series. Both parts have the same length, equal to the number of bytes
            of the module (little endian order).
        """
        session_key = self._gen_session_key()
        a = fpow(self._pb_key.g, session_key.k, self._pb_key.p)

        match data:
            case int():
                b = fpow(self._pb_key.y, session_key.k, self._pb_key.p) * data % self._pb_key.p
                return Elgamal.Ciphertext(a, b)

            case bytes():
                data = int.from_bytes(data, byteorder)
                b = fpow(self._pb_key.y, session_key.k, self._pb_key.p) * data % self._pb_key.p
                block_size = self.num_bytes_public_module
                return a.to_bytes(block_size, byteorder) + b.to_bytes(block_size, byteorder)

            case _:
                raise TypeError("Possible types: int, bytes.")

    def decrypt(self, data: Ciphertext or bytes, byteorder: Literal["big", "little"] = "big") -> int or bytes:
        """
        Method for decrypting data

        data
            Data to decrypt.
            - If the input data is of type Ciphertext, then the result of the method
            will be a number.
            - If the input data is of type bytes, then the output will be bytes less
            than 1 in length than the number of bytes in the module. The input string
            of bytes must contain serially connected numbers A and B in byte representation.
            The length of the total string must be the length of the module.
        """
        def transform(_a: int, _b: int) -> int:
            m1 = fpow(_a, self._pr_key.x, self._pr_key.p)
            m2 = modinv(m1, self._pr_key.p)
            m = m2 * _b % self._pr_key.p
            return m

        match data:
            case Elgamal.Ciphertext(a, b):
                return transform(a, b)

            case bytes():
                block_size = self.num_bytes_private_module
                a = int.from_bytes(data[:block_size], byteorder)
                b = int.from_bytes(data[block_size:], byteorder)
                return transform(a, b).to_bytes(block_size - 1, byteorder)

            case _:
                raise TypeError("Possible types: Elgamal.Ciphertext, bytes.")

    def make(self,
             data: int or Ciphertext or bytes,
             enc_proc: EncProc,
             byteorder: Literal["big", "little"] = "big"):
        """
        Method for encrypting and decrypting data.

        data
            Data to decrypt or encrypt.
            - (Encrypt) If the input data is of type int, then the result of the method will
            be a Ciphertext object containing two numbers A and B.
            - (Encrypt) If the input data is of type bytes, then the result of the method will
            be bytes that contain the number A and the number B, which are connected
            in series. Both parts have the same length, equal to the number of bytes
            of the module (little endian order).
            - (Decrypt) If the input data is of type Ciphertext, then the result of the method
            will be a number.
            - (Decrypt) If the input data is of type bytes, then the output will be bytes less
            than 1 in length than the number of bytes in the module. The input string
            of bytes must contain serially connected numbers A and B in byte representation.
            The length of the total string must be the length of the module.
            Encryption process. For the encryption process, use the EncProc enumeration.
        """
        match enc_proc:
            case EncProc.ENCRYPT:
                return self.encrypt(data, byteorder)

            case EncProc.DECRYPT:
                return self.decrypt(data, byteorder)

            case _:
                raise TypeError("Possible types: EncProc.ENCRYPT, EncProc.DECRYPT.")
