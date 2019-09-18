import time

from cryptopy import Hacker, Receiver, Sender, Unbreakable

c = Unbreakable()
keys = c.generate_keys()

s = Sender(cipher=c, key=keys[0])
r = Receiver(cipher=c, key=keys[1])

text = " This is a test message!"
print("Sender sending text:", text)
text_encrypted = s.operate_cipher(text)
print("Encrypted text:", text_encrypted)
text_decrypted = r.operate_cipher(text_encrypted)
print("Receiver decrypted text:", text_decrypted)

print("Attempting to hack the code:")

h = Hacker()

start = time.time()
hacked = h.decode(text_encrypted, c, 0.8)
end = time.time()

print(f"Hacker used {end-start} seconds to find the code: {hacked}")
