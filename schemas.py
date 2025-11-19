"""
Database Schemas for ShopWithHassan

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase of the class name.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal


class Car(BaseModel):
    """
    Cars available for sale
    Collection: "car"
    """
    make: str = Field(..., description="Manufacturer, e.g., Toyota")
    model: str = Field(..., description="Model, e.g., Premio")
    year: int = Field(..., ge=1980, le=2100, description="Year of manufacture")
    price: float = Field(..., ge=0, description="Asking price in KES")
    mileage_km: Optional[int] = Field(None, ge=0, description="Mileage in kilometers")
    transmission: Optional[Literal["Automatic", "Manual"]] = Field(
        None, description="Transmission type"
    )
    fuel: Optional[Literal["Petrol", "Diesel", "Hybrid", "Electric"]] = Field(
        None, description="Fuel type"
    )
    color: Optional[str] = Field(None, description="Exterior color")
    location: Optional[str] = Field(
        "Mombasa", description="Car location for viewing/delivery"
    )
    description: Optional[str] = Field(None, description="Extra details")
    image_url: Optional[str] = Field(None, description="Primary image URL")


class Request(BaseModel):
    """
    Leads for car purchase or delivery service
    Collection: "request"
    """
    name: str = Field(..., description="Customer full name")
    email: Optional[EmailStr] = Field(None, description="Customer email")
    phone: str = Field(..., description="Customer phone number")
    service_type: Literal["car-sale", "delivery-service"] = Field(
        ..., description="Type of inquiry"
    )
    preferred_car: Optional[str] = Field(
        None, description="Desired car (make/model) if buying"
    )
    location: Optional[str] = Field(
        "Mombasa", description="Pickup/delivery or viewing location"
    )
    message: Optional[str] = Field(None, description="Additional details")
    status: Literal["new", "in-progress", "completed"] = Field(
        "new", description="Lead status"
    )


# Keep example schemas for reference (not used by the app)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True


class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
