# The module contains an implementation of the Diffie-Hellman cryptographic protocol.
from dataclasses import dataclass
from random import randrange

from sympy import isprime

from app.crypto.utils import gen_prime
from app.crypto.mathlib import fpow


class DiffieHellman:

    @dataclass(frozen=True)
    class SharedKeys:
        g: int
        p: int

    @dataclass(frozen=True)
    class SharedPrivateKey:
        k: int

    @dataclass(frozen=True)
    class PrivateKey:
        k: int

    @dataclass(frozen=True)
    class PublicKey:
        k: int

    def __init__(self, private_key: PrivateKey, public_key: PublicKey, shared_keys: SharedKeys) -> None:
        """
        Implementation of the Diffie-Hellman cryptographic protocol.

        private_key
            Private key of type DiffieHellman.PrivateKey, which contains a number - the key.
        public_key
            Public key of type DiffieHellman.PublicKey, which contains a number - the key.
        shared_keys
            Shared keys of type DiffieHellman.SharedKeys, which contains the number primitive
            root G and the prime number P.
        """
        if not (isinstance(private_key, DiffieHellman.PrivateKey) and
                isinstance(public_key, DiffieHellman.PublicKey) and
                isinstance(shared_keys, DiffieHellman.SharedKeys)):
            raise TypeError("Arguments must be of type DiffieHellman.PrivateKey, "
                            "DiffieHellman.PublicKey and DiffieHellman.SharedKey.")

        self._shared_keys = shared_keys
        self._private_key = private_key
        self._public_key = public_key
        self._shared_private_key = None

    @property
    def public_key(self) -> PublicKey:
        """Get the value of the public key."""
        return self._public_key

    @property
    def private_key(self) -> PrivateKey:
        """Get the value of the private key."""
        return self._private_key

    @property
    def shared_private_key(self) -> SharedPrivateKey:
        """Get the value of the shared private key."""
        return self._shared_private_key

    @staticmethod
    def gen_shared_keys(n: int = 1024) -> SharedKeys:
        """Method for generating shared keys.

        n
            Number of bits of a prime number P.

        Returns
            Shared keys that have type DiffieHellman.SharedKeys.
        """
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

        return DiffieHellman.SharedKeys(g, p)

    @staticmethod
    def gen_keys(shared_keys: SharedKeys) -> tuple[PrivateKey, PublicKey]:
        """Method for generating private and public keys.

        shared_keys
            Shared keys of type DiffieHellman.SharedKeys, which contains the number primitive
            root G and the prime number P.

        Returns
            Tuple of two elements - private and public keys.
        """
        private_key = randrange(2, shared_keys.p)
        public_key = fpow(shared_keys.g, private_key, shared_keys.p)
        df = DiffieHellman
        return df.PrivateKey(private_key), df.PublicKey(public_key)

    def create_shared_private_key(self, other_public_key: PublicKey) -> None:
        """Method for creating and setting a user's private public key."""
        k = fpow(other_public_key.k, self._private_key.k, self._shared_keys.p)
        self._shared_private_key = DiffieHellman.SharedPrivateKey(k)

    def create_intermediate_key(self, other_intermediate_key: PublicKey) -> PublicKey:
        """Method for generating an intermediate key needed by other users."""
        k = fpow(other_intermediate_key.k, self._private_key.k, self._shared_keys.p)
        return DiffieHellman.PublicKey(k)
