import bcrypt

# Full names list
full_names = [
    "Abir Mohamed", "John Smith", "Annabel Key", "Tess Dunn", "Lilia Rowe",
    "Aaryan Mcclain", "Khadija Ahmed", "Zubair Horne", "Muna Muhumed", "Taylor Bennett",
    "Jordan Clarke", "Avery Morgan", "Casey Taylor", "Jamie Lee", "Riley Smith",
    "Morgan White", "Alex Johnson", "Sam Brown", "Jamie Green", "Avery Davis",
    "Jordan Thompson", "Casey Martin", "Taylor Wilson", "Jamie Harri"
]

# Hash and shorten password
def hash_and_shorten_password(name):
    # Hash with bcrypt and unique salt
    hashed_password = bcrypt.hashpw(name.encode('utf-8'), bcrypt.gensalt())

    # Take first 10 chars
    short_hash = hashed_password.decode('utf-8')[:10]

    return short_hash

# Create hashes for usernames (initial + surname)
hashed_passwords = {}
for full_name in full_names:
    first_name, surname = full_name.split(' ', 1)
    new_username = f"{first_name[0].upper()}{surname.capitalize()}"
    hashed_passwords[new_username] = hash_and_shorten_password(new_username)

# Print usernames and passwords
for username, short_hash in hashed_passwords.items():
    print(f"Username: {username} | Password : {short_hash}")