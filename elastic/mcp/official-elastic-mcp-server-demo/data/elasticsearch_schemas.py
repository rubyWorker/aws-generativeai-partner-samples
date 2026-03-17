"""
Elasticsearch schemas for Travel Advisory Application.
These schemas are intentionally flat (non-nested) for easier querying.
All string fields use text+keyword multi-field so the Elasticsearch MCP server
can reference field.keyword for sorting, filtering, and term queries.
Only `name`, `description`, `address`, `venue`, and similar free-text fields
are plain `text` (no .keyword sub-field).
"""

# Destinations index schema
destinations_schema = {
    "mappings": {
        "properties": {
            "destination_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "name": {"type": "text"},
            "city": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "country": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "continent": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "description": {"type": "text"},
            "best_season": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "climate": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "language": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "currency": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "timezone": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "safety_rating": {"type": "integer"},
            "popularity_score": {"type": "integer"},
            "cost_level": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "tags": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
        }
    }
}

# Attractions index schema
attractions_schema = {
    "mappings": {
        "properties": {
            "attraction_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "destination_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "name": {"type": "text"},
            "type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "description": {"type": "text"},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "address": {"type": "text"},
            "opening_hours": {"type": "text"},
            "closing_hours": {"type": "text"},
            "price_range": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "duration_minutes": {"type": "integer"},
            "accessibility": {"type": "boolean"},
            "rating": {"type": "float"},
            "tags": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "best_time_to_visit": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "crowd_level": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
        }
    }
}

# Hotels index schema
hotels_schema = {
    "mappings": {
        "properties": {
            "hotel_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "destination_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "name": {"type": "text"},
            "brand": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "address": {"type": "text"},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "star_rating": {"type": "integer"},
            "user_rating": {"type": "float"},
            "price_per_night": {"type": "float"},
            "currency": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "amenities": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "room_types": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "breakfast_included": {"type": "boolean"},
            "free_wifi": {"type": "boolean"},
            "parking_available": {"type": "boolean"},
            "distance_to_center_km": {"type": "float"},
            "pet_friendly": {"type": "boolean"},
            "check_in_time": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "check_out_time": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
        }
    }
}

# Travel advisories index schema
advisories_schema = {
    "mappings": {
        "properties": {
            "advisory_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "destination_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "country": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "advisory_level": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "description": {"type": "text"},
            "issue_date": {"type": "date"},
            "expiry_date": {"type": "date"},
            "issuing_authority": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "health_risks": {"type": "text"},
            "safety_risks": {"type": "text"},
            "entry_requirements": {"type": "text"},
            "visa_required": {"type": "boolean"},
            "vaccination_required": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "currency_restrictions": {"type": "text"},
            "local_laws": {"type": "text"},
            "emergency_contacts": {"type": "text"}
        }
    }
}

# Weather data index schema
weather_schema = {
    "mappings": {
        "properties": {
            "weather_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "destination_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "date": {"type": "date"},
            "temperature_high_celsius": {"type": "float"},
            "temperature_low_celsius": {"type": "float"},
            "precipitation_mm": {"type": "float"},
            "humidity_percent": {"type": "integer"},
            "wind_speed_kmh": {"type": "float"},
            "weather_condition": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "uv_index": {"type": "integer"},
            "air_quality_index": {"type": "integer"},
            "forecast_accuracy": {"type": "float"}
        }
    }
}

# Events index schema
events_schema = {
    "mappings": {
        "properties": {
            "event_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "destination_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "name": {"type": "text"},
            "type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "description": {"type": "text"},
            "start_date": {"type": "date"},
            "end_date": {"type": "date"},
            "venue": {"type": "text"},
            "address": {"type": "text"},
            "latitude": {"type": "float"},
            "longitude": {"type": "float"},
            "price_range": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "ticket_required": {"type": "boolean"},
            "booking_url": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "local_significance": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "crowd_expectation": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
        }
    }
}

# Users index schema
users_schema = {
    "mappings": {
        "properties": {
            "user_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "email": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "first_name": {"type": "text"},
            "last_name": {"type": "text"},
            "phone": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "date_of_birth": {"type": "date"},
            "nationality": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "preferred_language": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "preferred_currency": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "loyalty_tier": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "loyalty_points": {"type": "integer"},
            "account_created": {"type": "date"},
            "last_login": {"type": "date"},
            "preferences": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "dietary_restrictions": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "special_needs": {"type": "text"}
        }
    }
}

# Reservations index schema
reservations_schema = {
    "mappings": {
        "properties": {
            "reservation_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "user_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "hotel_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "room_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "check_in_date": {"type": "date"},
            "check_out_date": {"type": "date"},
            "num_guests": {"type": "integer"},
            "num_rooms": {"type": "integer"},
            "total_price": {"type": "float"},
            "currency": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "payment_status": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "payment_method": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "booking_date": {"type": "date"},
            "booking_source": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "status": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "special_requests": {"type": "text"},
            "breakfast_included": {"type": "boolean"},
            "is_refundable": {"type": "boolean"},
            "cancellation_deadline": {"type": "date"},
            "confirmation_code": {"type": "text", "fields": {"keyword": {"type": "keyword"}}}
        }
    }
}

# Room availability index schema
room_availability_schema = {
    "mappings": {
        "properties": {
            "availability_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "hotel_id": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "hotel_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "city": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "room_type": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "date": {"type": "date"},
            "available_rooms": {"type": "integer"},
            "total_rooms": {"type": "integer"},
            "price": {"type": "float"},
            "currency": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "promotion_code": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "discount_percentage": {"type": "float"},
            "minimum_stay": {"type": "integer"},
            "is_closed": {"type": "boolean"},
            "last_updated": {"type": "date"}
        }
    }
}

# All schemas in a dictionary for easy access
schemas = {
    "destinations": destinations_schema,
    "attractions": attractions_schema,
    "hotels": hotels_schema,
    "advisories": advisories_schema,
    "weather": weather_schema,
    "events": events_schema,
    "users": users_schema,
    "reservations": reservations_schema,
    "room_availability": room_availability_schema
}
