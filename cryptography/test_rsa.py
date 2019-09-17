from cryptopy import RSA, Receiver, Sender

rsa = RSA()

bob = Sender(cipher=rsa)
alice = Receiver(cipher=rsa)

keys = rsa.generate_keys()
# The first value is the encoding key

bob.set_key(keys[0])
alice.set_key(keys[1])

encoded = bob.operate_cipher("Hi Alice, this is a test message!")
print("The RSA256 encoded message is :\n", encoded, end="\n\n\n")

decoded = alice.operate_cipher(encoded)

print("Alice decoded the message to: \n", decoded, end="\n\n\n")
