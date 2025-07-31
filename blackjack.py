import random

card_suite = ['♡', '♢', '♧', '♤']
card_rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [(rank, suite) for suite in card_suite for rank in card_rank]

def card_values(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])
    

    
random.shuffle(deck)
player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]

while True:
    player_score = sum(card_values(card) for card in player_hand)
    dealer_score = sum(card_values(card) for card in dealer_hand)
    print(f"Your hand: {player_hand} (Score: {player_score})")
    print(f"Dealer's hand: {dealer_hand[0]}, Hidden Card")
    print("\n")
    choice = input("Do you want to (h)it or (s)tand? ").lower()
    if choice == 'h':
        new_card = deck.pop()
        player_hand.append(new_card)
    elif choice == 's':
        break
    else:
        print("Invalid choice, please choose 'h' or 's'.")
        continue

    if player_score > 21:
        print("Cards Dealer Has:", dealer_hand)
        print("Score Of The Dealer:", dealer_score)
        print("Cards Player Has:", player_hand)
        print("Score Of The Player:", player_score)
        print("Dealer wins (Player Loss Because Player Score is exceeding 21)")
        break

while dealer_score < 17:
    new_card = deck.pop()
    dealer_hand.append(new_card)
    dealer_score += card_values(new_card)

print("Cards Dealer Has:", dealer_hand)
print("Score Of The Dealer:", dealer_score)
print("\n")

if dealer_score > 21:
    print("Cards Dealer Has:", dealer_hand)
    print("Score Of The Dealer:", dealer_score)
    print("Cards Player Has:", player_hand)
    print("Score Of The Player:", player_score)
    print("Player wins (Dealer Loss Because Dealer Score is exceeding 21)")
elif player_score > dealer_score:
    print("Cards Dealer Has:", dealer_hand)
    print("Score Of The Dealer:", dealer_score)
    print("Cards Player Has:", player_hand)
    print("Score Of The Player:", player_score)
    print("Player wins (Player Has High Score than Dealer)")
elif dealer_score > player_score:
    print("Cards Dealer Has:", dealer_hand)
    print("Score Of The Dealer:", dealer_score)
    print("Cards Player Has:", player_hand)
    print("Score Of The Player:", player_score)
    print("Dealer wins (Dealer Has High Score than Player)")
else:
    print("Cards Dealer Has:", dealer_hand)
    print("Score Of The Dealer:", dealer_score)
    print("Cards Player Has:", player_hand)
    print("Score Of The Player:", player_score)
    print("It's a tie.")
