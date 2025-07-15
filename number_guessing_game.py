import random

secret_number = random.randint(1, 101)

guess = int(input("Guess a number between 1 and 100: "))

guess_counter = 0

while guess != secret_number and guess_counter < 3:
    if guess > int(secret_number):
        print("Your guess is too high.")
        guess_counter += 1
        guess = int(input("Try again: "))
    elif guess < int(secret_number):
        print("Your guess is too low.")
        guess_counter += 1
        guess = int(input("Try again: "))

if guess_counter == 3 and guess != secret_number:
    print("The number was: ", secret_number)
else:
    print("Congratulations! You've guessed the number:", secret_number)
