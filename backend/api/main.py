from fastapi import FastAPI
from backend.api.routes import bank1, bank2 ,suspicion, analytics
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Finance Backend 🚀")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Allow all during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register both bank APIs
app.include_router(bank1.router, prefix="/bank1", tags=["Bank1"])
app.include_router(bank2.router, prefix="/bank2", tags=["Bank2"])
app.include_router(suspicion.router)
app.include_router(analytics.router, prefix="/analytics")



@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Finance Backend"}
