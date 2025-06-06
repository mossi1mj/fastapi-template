from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import items, users

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Template Project",
    description="Reusable FastAPI starter project with modular structure",
    version="0.1.0"
)

# Allow cross-origin requests (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from different modules
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(items.router, prefix="/items", tags=["Items"])

# Default root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Template!"}
