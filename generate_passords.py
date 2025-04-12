import hashlib
import json


def generate_hashed_password(password):
    # Encode the password to bytes, then hash it using SHA-256
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password


# Dictionary containing team names and passwords
teams = {
    "admin"         : "butterscotch",
    "Souvik"        : "a",
    "Ansh"          : "b",
    "Swayamjit"     : "kundu15",
    "Bratanu"       : "c",
    "Rohan"         : "abc123",
    "Mohit"         : "bhannat",
    "Omm"           : "Rurushu1234",
    "Nirbhay"       : "Nirbhay18#",
    "Sahil"         : "johan.liebert",
    "Jitesh"        : "APR12Jitu",
    "Anshika"       : "d",
    "Aryan"         : "aryannn123",
    "Nehal"         : "f",
}

hashed_passwords = {}

# Generate hashed passwords for each team
for team, password in teams.items():
    hashed_password = generate_hashed_password(password)
    hashed_passwords[team] = hashed_password

for team, hashed_password in hashed_passwords.items():
    print(f"{team}: {hashed_password}")

# Write the hashed passwords to a JSON file
output_file = "static/users.json"
with open(output_file, "w") as file:
    json.dump(hashed_passwords, file, indent=4, sort_keys=True)

print(f"Hashed passwords have been written to {output_file}")
