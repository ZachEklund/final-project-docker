1) Executive Summary
Problem:
Many casual or beginner blackjack players struggle to make optimal decisions during play, often missing opportunities to double, split, or stand correctly. This can reduce winnings and increase losses. The goal of this project is to provide a fast, automated blackjack strategy advisor for players to get move recommendations in real-time.
Solution:
The Blackjack Advisor is a lightweight web API built with FastAPI that takes a player's hand and the dealer's upcard, then returns the recommended move using a simplified blackjack basic strategy. The app is fully containerized with Docker, so anyone can run it on their machine without installing dependencies manually. It also serves a static frontend for testing and demonstration.

2) System Overview
Course Concepts Integrated: FastAPI for creating a REST API, Docker for containerization and reproducible deployment, and Python functions implementing blackjack logic and basic strategy.
Architecture Diagram:
![alt text](<Screenshot 2025-11-30 at 10.04.57 PM.png>)
Data/Models/Services: No external datasets used; all logic is algorithmic. blackjack.py contains functions for hand evaluation and move recommendation. Formats: JSON requests/responses via REST API.

3) How To Run: Local
    # Build the Docker image
    docker build -t blackjack-advisor .

    # Run the container
    docker run --rm -p 8080:8000 blackjack-advisor

    # Test the API
    curl -X POST http://localhost:8080/advise \
      -H "Content-Type: application/json" \
      -d '{"player":["A","7"], "dealer":"9"}'
The frontend is accessible at http://localhost:8080/

4) Design Decisions

Why This Concept: FastAPI was chosen for its simplicity, speed, and built-in OpenAPI support, making it easy to serve both the API and static frontend. Docker ensures the environment is reproducible on any machine.

Alternatives Considered: 
Flask - simpler, but FastAPI provides automatic docs and async support.
Local virtual environments -  adds manual setup complexity for users.

Tradeoffs: 
Performance - Minimal CPU/memory usage; suitable for small-scale personal use.
Complexity - Straightforward logic and API design, no external DB required.
Maintainability - Modular blackjack.py makes updates easy.

Security/Privacy: 
No PII is processed.
API validates inputs to prevent runtime errors.

Ops Considerations:
Logs can be added via FastAPI middleware.
Limited scaling requirements since computations are lightweight.

5) Results & Evaluation
Sample Output (JSON response):
{
  "action": "Stand"
}
The app returns correct recommendations for various test hands. Unit tests are included in:
/tests/test_basic_strategypy.