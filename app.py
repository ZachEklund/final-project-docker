# app.py
from flask import Flask, request, jsonify
import os
from blackjack import basic_strategy, hand_value, normalize_card
from llm_provider import explain_decision

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/advise", methods=["POST"])
def advise():
    """
    POST JSON:
    {
      "player": ["A♠", "7♦"],
      "dealer": "6♣",
      "can_double": true,
      "can_split": true
    }
    """
    data = request.get_json() or {}
    player = data.get("player", [])
    dealer = data.get("dealer")
    can_double = data.get("can_double", True)
    can_split = data.get("can_split", True)

    if not player or not dealer:
        return jsonify({"error": "player and dealer required"}), 400

    # normalize cards (strip suits, accept 'A','K','Q','J' or numeric strings)
    player_norm = [normalize_card(c) for c in player]
    dealer_norm = normalize_card(dealer)

    decision = basic_strategy(player_norm, dealer_norm, can_double=can_double, can_split=can_split)
    # deterministic reasoning we can unit test
    explanation = explain_decision(
        provider=os.getenv("LLM_PROVIDER", "mock"),
        prompt={"player": player_norm, "dealer": dealer_norm, "decision": decision}
    )

    return jsonify({
        "player": player,
        "dealer": dealer,
        "decision": decision,
        "explanation": explanation
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)