import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Car, Request

app = FastAPI(title="ShopWithHassan API", description="Cars & Delivery service in Mombasa")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "name": "shopwithhassan",
        "service": ["car sales", "delivery"],
        "location": "Mombasa",
        "contact": {
            "phone": "+254748898310",
            "email": "hassannuur2018@gmail.com",
        },
        "message": "Welcome to ShopWithHassan API",
    }


# Public catalog endpoints
@app.post("/api/cars", response_model=dict)
def add_car(car: Car):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    inserted_id = create_document("car", car)
    return {"id": inserted_id, "status": "ok"}


@app.get("/api/cars", response_model=List[dict])
def list_cars():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    cars = get_documents("car", {}, limit=100)
    # Convert ObjectId to string
    for c in cars:
        if "_id" in c:
            c["id"] = str(c.pop("_id"))
    return cars


# Lead/request endpoints
@app.post("/api/requests", response_model=dict)
def create_request(req: Request):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    inserted_id = create_document("request", req)
    return {"id": inserted_id, "status": "received"}


@app.get("/api/requests", response_model=List[dict])
def list_requests(limit: Optional[int] = 50):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("request", {}, limit=limit or 50)
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return docs


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
