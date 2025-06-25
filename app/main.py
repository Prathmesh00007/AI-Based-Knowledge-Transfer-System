# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import settings
from endpoints import auth, ingest, record, search, test, ingest_confluence  # Import your endpoint routers
import uvicorn
# import your endpoint routers
# If you have search endpoints: from app.endpoints import search

app = FastAPI(title="Knowledge Transfer System")

# Add middleware (adjust CORS and session configs as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include endpoint routers
app.include_router(auth.router, prefix="")
app.include_router(ingest.router, prefix="")
app.include_router(record.router, prefix="")
app.include_router(search.router, prefix="")  
app.include_router(test.router, prefix="")
app.include_router(ingest_confluence.router, prefix="")  # If you have a test endpoint
# If you have a record endpoint
# app.include_router(search.router, prefix="")  # If you have a search endpoint


# Optionally, add a home endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Knowledge Transfer System"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
