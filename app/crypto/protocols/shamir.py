# The module contains an implementation of the Shamir cryptographic protocol.
from secrets import SystemRandom
from dataclasses import dataclass

from app.crypto.mathlib import ext_gcd, fpow


class Shamir:
    @dataclass
    class PrivateKey:
        k: int
        p: int

    @dataclass
    class PublicKey:
        k: int
        p: int

    def __init__(self, private_key: PrivateKey, public_key: PublicKey) -> None:
        """Implementation of the Shamir cryptographic protocol.

        private_key
            Private key of type Shamir.PrivateKey, which contains a number K and the prime number p - module.
        public_key
            Public key of type Shamir.Public, which contains a number K and the prime number p - module.
        """
        if not (isinstance(private_key, Shamir.PrivateKey) and isinstance(public_key, Shamir.PublicKey)):
            raise TypeError("Arguments must be of type Shamir.PrivateKey and Shamir.PublicKey.")

        self._private_key = private_key
        self._public_key = public_key

    def encrypt(self, data: int) -> int:
        """Method for encrypting data with a public key."""
        return fpow(data, self._public_key.k, self._public_key.p)

    def decrypt(self, data: int) -> int:
        """Method for decrypting data with a private key"""
        return fpow(data, self._private_key.k, self._private_key.p)

    @property
    def public_key(self) -> PublicKey:
        """Get the value of the public key."""
        return self._public_key

    @property
    def private_key(self) -> PrivateKey:
        """Get the value of the private key."""
        return self._private_key

    @staticmethod
    def gen_keys(p: int) -> tuple[PrivateKey, PublicKey]:
        """Method for generating private and public keys.

        p
            Large prime number.

        Returns
            Tuple of two elements - private and public keys.
        """
        phi = p - 1
        sysrand = SystemRandom()

        while True:
            public_key = sysrand.randrange(2, phi)
            d, private_key, _ = ext_gcd(public_key, phi)

            if d == 1:
                break

        private_key %= phi

        return Shamir.PrivateKey(private_key, p), Shamir.PublicKey(public_key, p)
