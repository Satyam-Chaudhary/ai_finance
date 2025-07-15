import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from backend.api.routes import bank1, bank2, suspicion, analytics, transactions
from backend.stream.kafka_consumer import consume_suspicious_messages
from fastapi.middleware.cors import CORSMiddleware
from backend.api.ws import router as ws_router

# Modern lifespan event handler to run Kafka in background
@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_task = asyncio.create_task(consume_suspicious_messages())
    print("🚀 Kafka consumer started in background.")
    yield
    kafka_task.cancel()
    try:
        await kafka_task
    except asyncio.CancelledError:
        print("🛑 Kafka consumer stopped.")

app = FastAPI(title="AI Finance Backend 🚀", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(transactions.router)
app.include_router(bank1.router, prefix="/bank1", tags=["Bank1"])
app.include_router(bank2.router, prefix="/bank2", tags=["Bank2"])
app.include_router(suspicion.router)
app.include_router(analytics.router, prefix="/analytics")
app.include_router(ws_router)

@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Finance Backend"}
