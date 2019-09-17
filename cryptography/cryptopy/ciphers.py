from linecache import getline
from random import randint

from .crypto_utils import (blocks_from_text, generate_random_prime,
                           modular_inverse, text_from_blocks)


class Cypher:
    """
    Superclass for all ciphers
    """

    def __init__(self):
        self.symbols = [chr(i) for i in range(32, 127)]
        self.symbol_count = len(self.symbols)

    def encode(self, content, key):
        """Encode a message using a key"""

    def decode(self, content, key):
        """Decode an encrypted message using a key
        :param content: string. the message to encode
        :param key: string | tuple<int> | int the key to be used for decoding
        """

    def generate_keys(self):
        """
        Generates a encryption_key, decryption_key pair
        :return A tuple with two keys
        """
        return (0, 0)

    def verify(self, content):
        """Verify that the ciphers encoding/decoding works"""
        keys = self.generate_keys()
        return content == self.decode(self.encode(content, keys[0]), keys[1])


class Ceasar(Cypher):
    """
    Cipher that uses ceasar encryption to encode/decode messages.
    """

    def generate_keys(self):
        key = randint(1, 9999)
        return (key, key)

    def encode(self, content, key):
        result = ""
        for char in content:
            new_value = key + self.symbols.index(char)
            result += self.symbols[new_value % self.symbol_count]
        return result

    def decode(self, content, key):
        result = ""
        for char in content:
            new_value = self.symbols.index(char) - key
            if new_value < 0:
                result += self.symbols[new_value % self.symbol_count]
            else:
                result += self.symbols[new_value]
        return result


class Multiplicative(Cypher):
    """
    Cipher that uses multiplicative encryption to encode/decode messages.
    """

    def generate_keys(self):
        # Generate keys by choosing a random number and finding the inverse.
        # Recurively finding key pairs if there does not exist an inverse
        key = randint(1, 9999)
        inv = modular_inverse(key, self.symbol_count)
        if not inv:
            return self.generate_keys()
        return (key, inv)

    def encode(self, content, key):
        result = ""
        for char in content:
            new_value = (self.symbols.index(char) * key) % self.symbol_count
            result += self.symbols[new_value]
        return result

    def decode(self, content, key):
        return self.encode(content, key)


class Affine(Cypher):
    """
    Cipher that combines ceasar and multiplicative encryption to encode/decode messages.
    """

    def __init__(self):
        super().__init__()
        # Create new instances of Ceasar and multiplicative
        self.ceasar = Ceasar()
        self.multi = Multiplicative()

    def generate_keys(self):
        mkeys = self.multi.generate_keys()
        ckeys = self.ceasar.generate_keys()
        return ((mkeys[0], ckeys[0]), (mkeys[1], ckeys[1]))

    def encode(self, content, key):
        return self.ceasar.encode(self.multi.encode(content, key[0]), key[1])

    def decode(self, content, key):
        return self.multi.decode(self.ceasar.decode(content, key[1]), key[0])


class Unbreakable(Cypher):
    """
    Cipher using the 'unbreakable' method to encrypt messages
    """

    def generate_keys(self):
        # Take a random word from the list of english words
        with open("english_words.txt") as file:
            word_count = len(file.readlines())
        key = getline("english_words.txt", randint(0, word_count - 1)).strip()
        # Calculate the inverse by iterating through the key and finding the appropriate "opposite"
        # symbol
        inv = "".join(
            [
                self.symbols[
                    self.symbol_count - (self.symbols.index(i) % self.symbol_count)
                ]
                for i in key
            ]
        )
        return (key, inv)

    def encode(self, content, key):
        result = ""
        # Loop through each character in the input string and encode it using the secret word.
        for i in range(len(content)):
            new_value = (
                self.symbols.index(content[i])
                + self.symbols.index(key[i % len(key) - 1])
            ) % self.symbol_count
            result += self.symbols[new_value]
        return result

    def decode(self, content, key):
        # simply encode the message using the decoding word
        return self.encode(content, key)


class RSA(Cypher):
    """
    Cipher using RSA to encrypt messages, defaults to 256 bits
    """

    def generate_keys(self, bits=256):
        # Generate prime pair, and make sure they are not the same
        p, q = 1, 1
        while p == q:
            q, p = generate_random_prime(bits), generate_random_prime(bits)

        n = p * q
        phi = (p - 1) * (q - 1)
        d = False
        # Make sure to choose a number where there is an inverse
        while not d:
            e = randint(3, phi - 1)
            d = modular_inverse(e, phi)

        # Return the keys as a tuple with keys as tuples
        return ((n, e), (n, d))

    def encode(self, content, key):
        blocks = blocks_from_text(content, 32)
        # Encode the content as a string consisting of numbers with bock size 32
        # the blocks are separated by spaces
        return "".join(
            [str(pow(block, key[1], key[0])) + " " for block in blocks]
        ).rstrip()

    def decode(self, content, key):
        blocks = content.split(" ")
        # Decode all the bblocks, and get the unicode string
        decoded_blocks = [pow(int(block), key[1], key[0]) for block in blocks]
        return text_from_blocks(decoded_blocks, 256)
