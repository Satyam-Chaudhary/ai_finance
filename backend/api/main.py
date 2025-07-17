import asyncio
import os
from fastapi import FastAPI
from contextlib import asynccontextmanager


from backend.api.routes import bank1, bank2, suspicion, analytics, transactions, auth
from backend.stream.kafka_consumer import consume_suspicious_messages
from fastapi.middleware.cors import CORSMiddleware
from backend.api.ws import router as ws_router
from backend.db import models, db
from backend import config


# db_url = config.DATABASE_URL
# if db_url.startswith("sqlite:///"):
#     db_file = db_url[len("sqlite:///"):]
#     # If it's a relative path, make it absolute
#     if not os.path.isabs(db_file):
#         db_file = os.path.abspath(db_file)
#     print("---" * 20)
#     print(f"✅ DATABASE FILE LOCATION: {db_file}")
#     print("---" * 20)


models.Base.metadata.create_all(bind=db.engine)

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

app = FastAPI(title="AI Finance Backend ", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all the routers
app.include_router(auth.router) 
app.include_router(transactions.router)
app.include_router(bank1.router, prefix="/bank1", tags=["Bank1"])
app.include_router(bank2.router, prefix="/bank2", tags=["Bank2"])
app.include_router(suspicion.router)
app.include_router(analytics.router, prefix="/analytics")
app.include_router(ws_router)


@app.get("/")
def root():
    return {"message": "Welcome to the AI-Powered Finance Backend"}
