from fastapi import APIRouter, HTTPException
from datetime import datetime
from pymongo import MongoClient
import os

router = APIRouter(tags=["Health"])

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")


@router.get("/health")
def health_check():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")

        return {
            "status": "healthy",
            "service": "FreshLense Backend",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )