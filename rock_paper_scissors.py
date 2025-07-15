# TODO : add option to choose if you want to play computer or human

input1 = input("Player 1, enter your choice (Rock, Paper, Scissors): ")
input2 = input("Player 2, enter your choice (Rock, Paper, Scissors): ")

def play_rps(player1, player2):
    input1 = player1.lower()
    input2 = player2.lower()

    if input1 == input2:
        return "It's a tie!"
    elif (input1 == "rock" and input2 == "scissors"):
        return "Player 1 wins! Rock crushes Scissors."
    elif (input1 == "scissors" and input2 == "paper"):
        return "Player 1 wins! Scissors cut Paper."
    elif (input1 == "paper" and input2 == "rock"):
        return "Player 1 wins! Paper covers Rock."
    elif (input2 == "rock" and input1 == "scissors"):
        return "Player 2 wins! Rock crushes Scissors."
    elif (input2 == "scissors" and input1 == "paper"):
        return "Player 2 wins! Scissors cut Paper."
    elif (input2 == "paper" and input1 == "rock"):
        return "Player 2 wins! Paper covers Rock."
    else:
        return "Invalid input! Please enter Rock, Paper, or Scissors."
    
print(play_rps(input1, input2))
