from flask import Flask, request, jsonify
from blackjack import build_prompt  # logic helper
from gpt_client import ask_gpt      # LLM call

app = Flask(__name__)

@app.route("/advise", methods=["POST"])
def advise():
    data = request.json
    player = data.get("player")
    dealer = data.get("dealer")

    if not player or not dealer:
        return jsonify({"error": "Missing player or dealer cards"}), 400

    # Build prompt for LLM
    prompt = build_prompt(player, dealer)

    # Call GPT
    try:
        advice = ask_gpt(prompt)
    except Exception as e:
        return jsonify({"error": "LLM request failed", "detail": str(e)}), 500

    return jsonify({"advice": advice})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
