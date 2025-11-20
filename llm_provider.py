import os
import json
import requests

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # "mock", "ollama", "azure"

def explain_decision(provider="mock", prompt=None):
    """
    prompt: dict {player: [...], dealer: '6', decision: 'hit'}
    Returns a string explanation.
    """
    if provider is None:
        provider = LLM_PROVIDER
    if provider == "mock":
        return _mock_explain(prompt)
    elif provider == "ollama":
        return _ollama_explain(prompt)
    elif provider == "azure":
        return _azure_explain(prompt)
    else:
        return _mock_explain(prompt)

def _mock_explain(p):
    player = p.get("player", [])
    dealer = p.get("dealer")
    decision = p.get("decision")
    return (f"Deterministic advisor: with player cards {player} "
            f"and dealer upcard {dealer}, the basic-strategy decision is '{decision}'. "
            "This decision is based on standard blackjack strategy tables considering hard/soft totals and pairs.")

# ---- Placeholder implementations follow.
# If you want me to enable live calls, I can fill these out with exact API usage.
def _ollama_explain(p):
    # Example: call local ollama HTTP API if installed.
    # You'll need to set OLLAMA_URL or use default http://localhost:11434
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    model = os.getenv("OLLAMA_MODEL", "llama2")  # set to your installed model
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful blackjack advisor."},
            {"role": "user", "content": f"Player {p.get('player')} Dealer {p.get('dealer')} Decision {p.get('decision')}. Explain briefly."}
        ],
        "max_tokens": 200
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        data = r.json()
        # adjust extraction depending on your Ollama response format
        return data.get("text") or json.dumps(data)
    except Exception as e:
        return f"[ollama explain failed: {e}]"

def _azure_explain(p):
    # Placeholder for Azure OpenAI or OpenAI-compatible endpoint.
    # Configure AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    if not (endpoint and key and deployment):
        return "[azure not configured: set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT_NAME]"
    # Example minimal request using 'requests' to Azure REST API - user must adapt to their account
    url = f"{endpoint}/openai/deployments/{deployment}/completions?api-version=2023-06-01-preview"
    headers = {"api-key": key, "Content-Type": "application/json"}
    prompt_text = f"Player {p.get('player')} Dealer {p.get('dealer')} Decision {p.get('decision')}. Explain in 2-3 sentences."
    payload = {"prompt": prompt_text, "max_tokens": 200, "temperature": 0}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        r.raise_for_status()
        data = r.json()
        # adjust extraction depending on Azure response format
        choices = data.get("choices", [])
        if choices:
            return choices[0].get("text", "") or str(data)
        return str(data)
    except Exception as e:
        return f"[azure explain failed: {e}]"