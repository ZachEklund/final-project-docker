from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os
import logging
import time

# ---- Observability Setup ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("blackjack_advisor")

app = FastAPI()

# Enable CORS so your frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    return response

# Serve static files from the 'frontend' folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve the index.html at the root
@app.get("/")
def read_index():
    return FileResponse(os.path.join("frontend", "index.html"))

# Health Check Endpoint (Ops)
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "blackjack-advisor"}

from blackjack import basic_strategy

# ---- API Model ----
class AdviceRequest(BaseModel):
    player: List[str]
    dealer: str

# ---- API Endpoint ----
@app.post("/advise")
def advise(req: AdviceRequest):
    try:
        # basic_strategy returns lowercase, so we title() it for display
        recommendation = basic_strategy(req.player, req.dealer).title()
        logger.info(f"Advice requested: Player={req.player}, Dealer={req.dealer} -> {recommendation}")
        return {"action": recommendation}
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return {"error": str(e)}

