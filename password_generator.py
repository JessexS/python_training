import random

length = int(input("Select how many letter password you want: "))

ascii_letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
special_characters = "!@#$%^&*()-_=[]{+}|;:,.<>?/"
numbers = "0123456789"

def generate_password(length):
    if length < 5:
        print("Password length should be at least 5 characters.")
    elif length >= 5:
       characters = ascii_letters + special_characters + numbers
       return characters

print("Your password has been generated")

if length == 5 or length == 6 or length == 7 or length == 8:
    print("Your password is cracked instantly!")
elif length == 9:
    print("Your password is cracked in 6 hours!")
elif length == 10:
    print("Your password is cracked in 2 weeks!")
elif length == 11:
    print("Your password is cracked in 3 years!")
elif length == 12:
    print("Your password is cracked in 226 years!")
elif length > 13:
    print("Your password is cracked in 15 000 years or more!")

print("Do you want to save your password? (yes/no)")
save_password = input().strip().lower()
if save_password == "yes":
    with open("password.txt", "w") as file:
        file.write(''.join(random.sample(generate_password(length), length)))
    print("Password saved to password.txt in this directory.")
else:
    print("Password not saved.")
