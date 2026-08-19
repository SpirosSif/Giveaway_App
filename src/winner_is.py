import json
import random

def draw_winner():
    with open("data/solo_usernames.json", "r", encoding="utf-8") as file:
        participants = json.load(file)
    print(participants[0])

    r=random.randint(0, 1000000)
    winner= participants[r % len(participants)]
    print("winner is " + winner)
    
    return winner