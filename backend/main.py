from fastapi import FastAPI
from mock_apis import bank1, bank2  # 👈 now importing bank2 too

app = FastAPI(title="AI Finance Backend 🚀")

# Register both bank APIs
app.include_router(bank1.router, prefix="/bank1", tags=["Bank1"])
app.include_router(bank2.router, prefix="/bank2", tags=["Bank2"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Finance Backend"}
