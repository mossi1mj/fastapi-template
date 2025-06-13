import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, plaid
from app.database import initialize_database
from app.models.user import User
from app.dependencies import initialize_firebase

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Template Project",
    description="Reusable FastAPI starter project with modular structure",
    version="0.1.0"
)

# Allow cross-origin requests (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
initialize_database([User])

# Initialize Firebase
initialize_firebase()

# Include routers from different modules
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(plaid.router, prefix="/plaid", tags=["Plaid"])
logger.info("FastAPI application started.")

# Default root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Template!"}
