from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import signals, assets

# Create all tables in the database.
# This is a simple approach for getting started.
# For production, you would use a migration tool like Alembic.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KIS Invest Assistant API",
    description="API for real-time stock analysis and portfolio management using KIS API.",
    version="0.1.0",
)

# CORS Middleware Setup
origins = [
    "http://localhost:3000",  # React default dev server
    # Add deployed frontend URLs here, e.g., "https://your-frontend.vercel.app"
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the KIS Invest Assistant API"}

# Include the API routers
app.include_router(signals.router, prefix="/signals", tags=["Analysis Signals"])
app.include_router(assets.router, prefix="/assets", tags=["Asset Management"])

# In the next steps, we will include the auth router here.
# from .routers import auth
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
