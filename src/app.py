from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# Enable CORS so your frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the 'frontend' folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve the index.html at the root
@app.get("/")
def read_index():
    return FileResponse(os.path.join("frontend", "index.html"))

# ---- Blackjack Logic ----
def hand_value(cards):
    total = 0
    aces = 0
    for c in cards:
        if c in ["J", "Q", "K"]:
            total += 10
        elif c == "A":
            aces += 1
            total += 11
        else:
            total += int(c)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def is_soft(cards):
    total = 0
    aces = 0
    for c in cards:
        if c in ["J", "Q", "K"]:
            total += 10
        elif c == "A":
            total += 11
            aces += 1
        else:
            total += int(c)
    return aces > 0 and total <= 21

def basic_strategy(player_cards, dealer_card):
    player_total = hand_value(player_cards)
    dealer_value = 10 if dealer_card in ["J", "Q", "K"] else (11 if dealer_card == "A" else int(dealer_card))

    # Soft hands
    if is_soft(player_cards):
        if player_total <= 17:
            return "Hit"
        if player_total == 18:
            return "Stand" if dealer_value in [2, 7, 8] else "Hit"
        return "Stand"

    # Hard hands
    if player_total <= 8:
        return "Hit"
    if player_total == 9:
        return "Hit" if dealer_value in [2, 7, 8, 9, 10, 11] else "Double or Hit"
    if 10 <= player_total <= 11:
        return "Double or Hit"
    if player_total == 12:
        return "Hit" if dealer_value in [2, 3, 7, 8, 9, 10, 11] else "Stand"
    if 13 <= player_total <= 16:
        return "Stand" if dealer_value in [2, 3, 4, 5, 6] else "Hit"
    return "Stand"  # 17 or more

# ---- API Model ----
class AdviceRequest(BaseModel):
    player: List[str]
    dealer: str

# ---- API Endpoint ----
@app.post("/advise")
def advise(req: AdviceRequest):
    try:
        recommendation = basic_strategy(req.player, req.dealer)
        return {"action": recommendation}
    except Exception as e:
        return {"error": str(e)}

