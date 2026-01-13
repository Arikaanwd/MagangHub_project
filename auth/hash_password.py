import hashlib

password = "admin123"
password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

print("Password :", password)
print("Hash     :", password_hash)
