from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import subprocess

# Decapsulate
subprocess.run(["openssl", "pkeyutl", "-decap",
    "-inkey", "priv.pem",
    "-in", "kem.bin",
    "-secret", "recovered.bin"])

# Load recovered key
key = open("recovered.bin", "rb").read(32)
import os
os.remove("recovered.bin")

# Read combined file — first 12 bytes are IV, rest is ciphertext
combined = open("encrypted.bin", "rb").read()
iv = combined[:12]
ciphertext = combined[12:]

# Decrypt
plaintext = AESGCM(key).decrypt(iv, ciphertext, None)
open("decrypted.txt", "wb").write(plaintext)

print("Decryption successful")
