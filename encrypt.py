from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import subprocess

# Generate keypair
subprocess.run(["openssl", "genpkey", "-algorithm", "ML-KEM-768", "-out", "priv.pem"])
subprocess.run(["openssl", "pkey", "-in", "priv.pem", "-pubout", "-out", "pub.pem"])

# Encapsulate
subprocess.run(["openssl", "pkeyutl", "-encap",
    "-inkey", "pub.pem", "-pubin",
    "-secret", "secret.bin",
    "-out", "kem.bin"])

# Load secret as AES key
key = open("secret.bin", "rb").read(32)
os.remove("secret.bin")

# Generate IV and encrypt
iv = os.urandom(12)
plaintext = open("myfile.txt", "rb").read()
ciphertext = AESGCM(key).encrypt(iv, plaintext, None)

# Save iv and ciphertext together in one file
combined = iv + ciphertext
open("encrypted.bin", "wb").write(combined)

print("Encryption successful")
print("Files needed for decryption: encrypted.bin, kem.bin, priv.pem")
