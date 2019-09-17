import mmap
import re

from .ciphers import RSA, Affine, Ceasar, Multiplicative, Unbreakable


class Person:
    """
    Class for a person that interacts with a cipher.
    """

    def __init__(self, **kwargs):
        key = kwargs.get("key", None)
        cipher = kwargs.get("cipher", None)
        if key:
            self.key = key
        if cipher:
            self.cipher = cipher

    def set_key(self, key):
        self.key = key

    def get_key(self, key):
        return self.key

    def operate_cipher(self):
        return


class Sender(Person):
    """
    A receiver of an encoded message
    """

    def operate_cipher(self, content):
        return self.cipher.encode(content, self.key)


class Receiver(Person):
    """
    A sender of an encoded message.
    """

    def operate_cipher(self, content):
        return self.cipher.decode(content, self.key)


class Hacker(Person):
    """
    Hacker class to brute force ciphers
    """

    def check_message(self, content):
        """Returns the fraction of words are legal words"""
        words = re.sub("[!,.?:;@#]", "", content).split()
        try:
            with open("english_words.txt", "rb", 0) as file, mmap.mmap(
                file.fileno(), 0, access=mmap.ACCESS_READ
            ) as s:
                return (
                    len(words)
                    - [s.find(word.lower().encode("utf-8")) for word in words].count(-1)
                ) / len(words)
        except:
            return 0

    def decode(self, content, cipher, hit=0.5):
        """
        Attempt to brute force a cipher, given an encoded message
        :param hit=0.5: the amount of words needed to match for the encoded messsage to be
        acceptable
        """
        success = False
        key = 0
        while not success:
            decoded = cipher.decode(content, key)
            hitrate = self.check_message(decoded)
            if hitrate >= hit:
                success = True
            else:
                key += 1

        return decoded
