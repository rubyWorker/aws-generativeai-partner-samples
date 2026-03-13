#!/usr/bin/env python3
"""
Script to generate user profiles and their hotel reservations.
This script creates sample users with reservation history and loads them into Elasticsearch.
"""

import json
import random
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import faker
import argparse
from elasticsearch_schemas import schemas
from dotenv import load_dotenv
import os

# Initialize Faker
fake = faker.Faker()

# Base date for data generation (2026-2028 range, no 2025 data)
BASE_DATE = datetime(2026, 3, 9)

# Sample user data
SAMPLE_USERS = [
    {
        "user_id": "USER001",
        "email": "john.smith@example.com",
        "first_name": "John",
        "last_name": "Smith",
        "phone": "+1-555-123-4567",
        "date_of_birth": "1985-06-15",
        "nationality": "United States",
        "preferred_language": "English",
        "preferred_currency": "USD",
        "loyalty_tier": "Gold",
        "loyalty_points": 5000,
        "account_created": "2020-03-10",
        "last_login": "2026-03-08",
        "preferences": ["Non-smoking", "High floor", "King bed"],
        "dietary_restrictions": ["None"],
        "special_needs": ""
    },
    {
        "user_id": "USER002",
        "email": "maria.garcia@example.com",
        "first_name": "Maria",
        "last_name": "Garcia",
        "phone": "+34-611-234-567",
        "date_of_birth": "1990-11-22",
        "nationality": "Spain",
        "preferred_language": "Spanish",
        "preferred_currency": "EUR",
        "loyalty_tier": "Silver",
        "loyalty_points": 2500,
        "account_created": "2021-07-15",
        "last_login": "2026-03-07",
        "preferences": ["Quiet room", "Twin beds", "Near elevator"],
        "dietary_restrictions": ["Vegetarian"],
        "special_needs": ""
    },
    {
        "user_id": "USER003",
        "email": "akira.tanaka@example.com",
        "first_name": "Akira",
        "last_name": "Tanaka",
        "phone": "+81-90-1234-5678",
        "date_of_birth": "1978-09-03",
        "nationality": "Japan",
        "preferred_language": "Japanese",
        "preferred_currency": "JPY",
        "loyalty_tier": "Platinum",
        "loyalty_points": 12000,
        "account_created": "2019-01-20",
        "last_login": "2026-03-09",
        "preferences": ["Non-smoking", "Japanese breakfast", "Late check-out"],
        "dietary_restrictions": ["No pork"],
        "special_needs": "Accessible bathroom"
    },
    {
        "user_id": "USER004",
        "email": "alex.demo@example.com",
        "first_name": "Alex",
        "last_name": "Demo",
        "phone": "+1-555-987-6543",
        "date_of_birth": "1992-04-18",
        "nationality": "United States",
        "preferred_language": "English",
        "preferred_currency": "USD",
        "loyalty_tier": "Platinum",
        "loyalty_points": 15000,
        "account_created": "2019-06-01",
        "last_login": "2026-03-09",
        "preferences": ["Non-smoking", "High floor", "King bed", "Late check-out"],
        "dietary_restrictions": ["None"],
        "special_needs": ""
    }
]

def load_hotels(es_client):
    """Load hotels from Elasticsearch to use in reservations."""
    query = {
        "query": {
            "match_all": {}
        },
        "size": 100
    }
    
    response = es_client.search(index="hotels", body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]

def load_destination_city_map(es_client):
    """Load a mapping of destination_id -> city from Elasticsearch."""
    query = {
        "query": {"match_all": {}},
        "size": 100,
        "_source": ["destination_id", "city"]
    }
    try:
        response = es_client.search(index="destinations", body=query)
        return {hit["_source"]["destination_id"]: hit["_source"]["city"] for hit in response["hits"]["hits"]}
    except Exception as e:
        print(f"Warning: Could not load destination city map: {e}")
        return {}

def generate_past_reservations(user, hotels, num_reservations=3):
    """Generate past hotel reservations for a user."""
    reservations = []
    
    # Get current date
    now = BASE_DATE
    
    for i in range(num_reservations):
        # Select a random hotel
        hotel = random.choice(hotels)
        
        # Generate a random past date (between 30 and 365 days ago)
        days_ago = random.randint(30, 365)
        check_in_date = now - timedelta(days=days_ago)
        
        # Stay duration between 1 and 7 days
        stay_duration = random.randint(1, 7)
        check_out_date = check_in_date + timedelta(days=stay_duration)
        
        # Booking date (1-30 days before check-in)
        booking_days_before = random.randint(1, 30)
        booking_date = check_in_date - timedelta(days=booking_days_before)
        
        # Generate reservation
        reservation_id = f"{user['user_id']}_RES{i+1:03d}"
        room_type = random.choice(hotel.get("room_types", ["Standard"]))
        num_guests = random.randint(1, 4)
        price_per_night = hotel.get("price_per_night", 100)
        total_price = round(price_per_night * stay_duration * (1 + 0.1 * num_guests), 2)  # Simple price calculation
        
        reservation = {
            "reservation_id": reservation_id,
            "user_id": user["user_id"],
            "hotel_id": hotel["hotel_id"],
            "room_type": room_type,
            "check_in_date": check_in_date.strftime("%Y-%m-%d"),
            "check_out_date": check_out_date.strftime("%Y-%m-%d"),
            "num_guests": num_guests,
            "num_rooms": 1,
            "total_price": total_price,
            "currency": hotel.get("currency", "USD"),
            "payment_status": "Paid",
            "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
            "booking_date": booking_date.strftime("%Y-%m-%d"),
            "booking_source": random.choice(["Direct", "Expedia", "Booking.com", "Travel Agent"]),
            "status": "Completed",
            "special_requests": random.choice(["", "Late check-in", "Extra pillows", "Quiet room"]),
            "breakfast_included": hotel.get("breakfast_included", False),
            "is_refundable": random.choice([True, False]),
            "cancellation_deadline": (check_in_date - timedelta(days=1)).strftime("%Y-%m-%d"),
            "confirmation_code": f"CONF{random.randint(10000, 99999)}"
        }
        
        reservations.append(reservation)
    
    return reservations

def generate_future_reservations(user, hotels, num_reservations=1):
    """Generate future hotel reservations for a user."""
    reservations = []
    
    # Get current date
    now = BASE_DATE
    
    for i in range(num_reservations):
        # Select a random hotel
        hotel = random.choice(hotels)
        
        # Generate a random future date (between 7 and 180 days from now)
        days_ahead = random.randint(7, 180)
        check_in_date = now + timedelta(days=days_ahead)
        
        # Stay duration between 1 and 10 days
        stay_duration = random.randint(1, 10)
        check_out_date = check_in_date + timedelta(days=stay_duration)
        
        # Booking date (between now and 30 days ago)
        booking_days_ago = random.randint(0, 30)
        booking_date = now - timedelta(days=booking_days_ago)
        
        # Generate reservation
        reservation_id = f"{user['user_id']}_RES{i+4:03d}"  # Start from 4 to avoid overlap with past reservations
        room_type = random.choice(hotel.get("room_types", ["Standard"]))
        num_guests = random.randint(1, 4)
        price_per_night = hotel.get("price_per_night", 100)
        total_price = round(price_per_night * stay_duration * (1 + 0.1 * num_guests), 2)  # Simple price calculation
        
        reservation = {
            "reservation_id": reservation_id,
            "user_id": user["user_id"],
            "hotel_id": hotel["hotel_id"],
            "room_type": room_type,
            "check_in_date": check_in_date.strftime("%Y-%m-%d"),
            "check_out_date": check_out_date.strftime("%Y-%m-%d"),
            "num_guests": num_guests,
            "num_rooms": 1,
            "total_price": total_price,
            "currency": hotel.get("currency", "USD"),
            "payment_status": random.choice(["Paid", "Pending"]),
            "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
            "booking_date": booking_date.strftime("%Y-%m-%d"),
            "booking_source": random.choice(["Direct", "Expedia", "Booking.com", "Travel Agent"]),
            "status": "Confirmed",
            "special_requests": random.choice(["", "Early check-in", "Airport shuttle", "Birthday decoration"]),
            "breakfast_included": hotel.get("breakfast_included", False),
            "is_refundable": random.choice([True, False]),
            "cancellation_deadline": (check_in_date - timedelta(days=1)).strftime("%Y-%m-%d"),
            "confirmation_code": f"CONF{random.randint(10000, 99999)}"
        }
        
        reservations.append(reservation)
    
    return reservations



def generate_room_availability():
    """Generate event-centric room availability data using real hotels from DESTINATION_HOTELS.

    Only generates availability for:
    - A 30-day general window from BASE_DATE
    - ±3 days around each event in DESTINATION_EVENTS
    This keeps the dataset small and fast to load into Elasticsearch.

    Hotel IDs are generated to match the scheme used by generate_data.py so that
    room_availability records can be cross-referenced with the hotels index.
    """
    from real_world_data import DESTINATION_EVENTS, DESTINATION_HOTELS, REAL_DESTINATIONS

    # Build city -> dest_id mapping (same ordering as generate_data.py)
    city_to_dest_id = {}
    for i, dest in enumerate(REAL_DESTINATIONS):
        city_to_dest_id[dest["city"]] = f"DEST{i+1:04d}"

    # Build (city, hotel_name) -> hotel_id mapping using same scheme as generate_data.py
    hotel_id_map = {}
    num_hotels_per_dest = 5  # matches DEFAULT_NUM_HOTELS_PER_DEST in generate_data.py
    for city, hotels_list in DESTINATION_HOTELS.items():
        dest_id = city_to_dest_id.get(city)
        if not dest_id:
            continue
        for i, hotel_data in enumerate(hotels_list[:num_hotels_per_dest]):
            hotel_id_map[(city, hotel_data["name"])] = f"{dest_id}_HOTEL{i+1:03d}"

    availability_records = []
    now = BASE_DATE

    # Parse event dates into datetime ranges
    month_dict = {
        "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
        "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }

    room_types_config = [
        ("Standard", 1.0),
        ("Deluxe", 1.5),
        ("Suite", 2.0),
    ]

    # Currency map by city
    city_currency = {d["city"]: d["currency"] for d in REAL_DESTINATIONS}

    for city, hotels in DESTINATION_HOTELS.items():
        events = DESTINATION_EVENTS.get(city, [])
        currency = city_currency.get(city, "USD")

        # Collect all dates we need availability for
        target_dates = set()

        # 1) General 30-day window from BASE_DATE
        for d in range(30):
            target_dates.add(now + timedelta(days=d))

        # 2) ±3 days around each event (for current and next year)
        for evt in events:
            try:
                s_parts = evt["start_date"].strip().split()
                e_parts = evt["end_date"].strip().split()
                s_month = month_dict.get(s_parts[0])
                s_day = int(s_parts[1])
                e_month = month_dict.get(e_parts[0])
                e_day = int(e_parts[1])
                if not (s_month and e_month):
                    continue
                for year in [now.year, now.year + 1]:
                    try:
                        start_dt = datetime(year, s_month, s_day)
                        end_year = year if (e_month, e_day) >= (s_month, s_day) else year + 1
                        end_dt = datetime(end_year, e_month, e_day)
                        # Add ±3 days buffer
                        cursor = start_dt - timedelta(days=3)
                        while cursor <= end_dt + timedelta(days=3):
                            target_dates.add(cursor)
                            cursor += timedelta(days=1)
                    except ValueError:
                        pass
            except (ValueError, IndexError, KeyError):
                pass

        # Sort dates for consistent output
        sorted_dates = sorted(target_dates)

        # Pre-compute event ranges for pricing
        event_ranges = []
        for evt in events:
            try:
                s_parts = evt["start_date"].strip().split()
                e_parts = evt["end_date"].strip().split()
                s_month = month_dict.get(s_parts[0])
                s_day = int(s_parts[1])
                e_month = month_dict.get(e_parts[0])
                e_day = int(e_parts[1])
                if not (s_month and e_month):
                    continue
                for year in [now.year, now.year + 1]:
                    try:
                        start_dt = datetime(year, s_month, s_day)
                        end_year = year if (e_month, e_day) >= (s_month, s_day) else year + 1
                        end_dt = datetime(end_year, e_month, e_day)
                        event_ranges.append((start_dt, end_dt))
                    except ValueError:
                        pass
            except (ValueError, IndexError, KeyError):
                pass

        for hotel_info in hotels[:num_hotels_per_dest]:
            hotel_name = hotel_info["name"]
            # Use the same hotel_id as the hotels index
            hotel_id = hotel_id_map.get((city, hotel_name))
            if not hotel_id:
                # Fallback: generate from name (shouldn't happen if data is consistent)
                hotel_id = hotel_name.replace(" ", "_").replace(",", "").replace("'", "").upper()[:30]
            base_price = random.choice([150, 200, 250, 300, 350, 400]) if hotel_info.get("star_rating", 4) >= 5 else random.choice([80, 100, 120, 150])

            for room_type, type_multiplier in room_types_config:
                total_rooms = random.randint(5, 20)

                for date in sorted_dates:
                    date_str = date.strftime("%Y-%m-%d")
                    is_event_period = any(start <= date <= end for start, end in event_ranges)

                    # Availability — always guarantee bookable rooms so the demo works
                    if is_event_period:
                        # High demand during events, but always keep at least 2 rooms
                        available_rooms = max(2, total_rooms - random.randint(0, total_rooms // 2))
                    else:
                        # Normal period — plenty of availability
                        available_rooms = max(3, total_rooms - random.randint(0, total_rooms // 3))

                    # Pricing
                    price_multiplier = type_multiplier
                    if date.weekday() >= 5:
                        price_multiplier *= 1.2
                    if 5 <= date.month <= 8:
                        price_multiplier *= 1.3
                    if is_event_period:
                        price_multiplier *= 1.5

                    price = round(base_price * price_multiplier, 2)
                    availability_id = f"{hotel_id}_{room_type}_{date_str}"

                    availability_records.append({
                        "availability_id": availability_id,
                        "hotel_id": hotel_id,
                        "hotel_name": hotel_name,
                        "city": city,
                        "room_type": room_type,
                        "date": date_str,
                        "available_rooms": available_rooms,
                        "total_rooms": total_rooms,
                        "price": price,
                        "currency": currency,
                        "promotion_code": "" if random.random() > 0.1 else f"PROMO{random.randint(100, 999)}",
                        "discount_percentage": 0 if random.random() > 0.1 else random.choice([5, 10, 15, 20]),
                        "minimum_stay": 1 if random.random() > 0.2 else random.randint(2, 3),
                        "is_closed": False,
                        "last_updated": BASE_DATE.strftime("%Y-%m-%d")
                    })

    print(f"Generated {len(availability_records)} room availability records across {len(DESTINATION_HOTELS)} cities")
    return availability_records



def create_index(es_client, index_name, schema):
    """Create an Elasticsearch index with the given schema."""
    try:
        es_client.indices.create(index=index_name, body=schema)
        print(f"Created index: {index_name}")
    except Exception as e:
        if "resource_already_exists_exception" in str(e):
            print(f"Index {index_name} already exists. Skipping creation.")
        else:
            print(f"Error creating index {index_name}: {e}")

def index_documents(es_client, index_name, documents):
    """Index documents into Elasticsearch."""
    actions = [
        {
            "_index": index_name,
            "_source": document
        }
        for document in documents
    ]
    
    success, failed = bulk(es_client, actions, refresh=True)
    print(f"Indexed {success} documents into {index_name}. Failed: {failed}")

def save_to_json(data, filename):
    """Save data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved data to {filename}")

def connect_to_elasticsearch(args):
    """Connect to Elasticsearch using either local connection or cloud credentials."""
    try:
        # Try to load environment variables for cloud connection
        load_dotenv()
        es_api_key = os.getenv("ES_API_KEY")
        es_url = os.getenv("ES_URL")
        #es_cloud_id = os.getenv("ES_CLOUD_ID")
        if es_api_key and es_url:
            print("Connecting to Elasticsearch Serverless...")
            return Elasticsearch(hosts=[es_url],
            api_key=es_api_key,
            verify_certs=True,
            request_timeout=30)
            
        else:
            print(f"Connecting to Elasticsearch at {args.es_host}:{args.es_port}...")
            return Elasticsearch([{'host': args.es_host, 'port': args.es_port, 'scheme': 'http'}])
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate user profiles and reservations for Travel Advisory Application')
    parser.add_argument('--es-host', default='localhost', help='Elasticsearch host')
    parser.add_argument('--es-port', default=9200, type=int, help='Elasticsearch port')
    parser.add_argument('--save-json', action='store_true', help='Save generated data to JSON files')
    parser.add_argument('--load-es', action='store_true', help='Load data into Elasticsearch')
    parser.add_argument('--cleanup', action='store_true', help='Delete user indices before loading data')
    parser.add_argument('--delete-indices', action='store_true', help='Only delete user indices without loading new data')
    
    args = parser.parse_args()
    
    # Connect to Elasticsearch if needed for cleanup or loading
    if args.cleanup or args.load_es or args.delete_indices:
        #load_dotenv()
        es = connect_to_elasticsearch(args)
        #es_api_key = os.getenv("ES_API_KEY")
        #es_cloud_id = os.getenv("ES_CLOUD_ID")
        
        #if es_api_key and es_cloud_id:
        #    print("Connecting to Elasticsearch Cloud...")
        #    es = Elasticsearch(cloud_id=es_cloud_id, api_key=es_api_key)
        #else:
        #    print(f"Connecting to Elasticsearch at {args.es_host}:{args.es_port}...")
        #    es = Elasticsearch([{'host': args.es_host, 'port': args.es_port, 'scheme': 'http'}])
        
        # Delete indices if requested
        if args.cleanup or args.delete_indices:
            print("Cleaning up user-related Elasticsearch indices...")
            delete_user_indices(es)
            
            if args.delete_indices:
                print("User indices deletion complete!")
                return
    
    # Connect to Elasticsearch to load hotels
    if args.load_es:
        if 'es' not in locals():
            es = connect_to_elasticsearch(args)
            #load_dotenv()
            #es_api_key = os.getenv("ES_API_KEY")
            #es_cloud_id = os.getenv("ES_CLOUD_ID")
            
            #if es_api_key and es_cloud_id:
            #    print("Connecting to Elasticsearch Cloud...")
            #    es = Elasticsearch(cloud_id=es_cloud_id, api_key=es_api_key)
            #else:
            #    print(f"Connecting to Elasticsearch at {args.es_host}:{args.es_port}...")
            #    es = Elasticsearch([{'host': args.es_host, 'port': args.es_port, 'scheme': 'http'}])
        
        # Load hotels to use in reservations
        hotels = load_hotels(es)
        if not hotels:
            print("No hotels found in Elasticsearch. Please load hotel data first.")
            return
    else:
        # Dummy hotels for JSON output
        hotels = [
            {
                "hotel_id": "DUMMY_HOTEL001",
                "name": "Grand Hotel",
                "room_types": ["Standard", "Deluxe", "Suite"],
                "price_per_night": 150,
                "currency": "USD",
                "breakfast_included": True
            },
            {
                "hotel_id": "DUMMY_HOTEL002",
                "name": "Beach Resort",
                "room_types": ["Standard", "Ocean View", "Villa"],
                "price_per_night": 200,
                "currency": "USD",
                "breakfast_included": True
            },
            {
                "hotel_id": "DUMMY_HOTEL003",
                "name": "City Center Hotel",
                "room_types": ["Standard", "Business", "Executive Suite"],
                "price_per_night": 120,
                "currency": "EUR",
                "breakfast_included": False
            }
        ]
    
    # Generate reservations for each user
    all_reservations = []
    for user in SAMPLE_USERS:
        past_reservations = generate_past_reservations(user, hotels, 3)
        future_reservations = generate_future_reservations(user, hotels, 1)
        all_reservations.extend(past_reservations)
        all_reservations.extend(future_reservations)
    
    # Generate room availability data (event-centric, uses DESTINATION_HOTELS directly)
    room_availability = generate_room_availability()
    
    # Save to JSON if requested
    if args.save_json:
        save_to_json(SAMPLE_USERS, 'users.json')
        save_to_json(all_reservations, 'reservations.json')
        save_to_json(room_availability, 'room_availability.json')
    
    # Load into Elasticsearch if requested
    if args.load_es:
        if 'es' not in locals():
            es = connect_to_elasticsearch(args)
            #load_dotenv()
            #es_api_key = os.getenv("ES_API_KEY")
            #es_url = os.getenv("ES_URL")
        
            #not needed for serverless
            #es_cloud_id = os.getenv("ES_CLOUD_ID")
        
            #if es_api_key and es_url:
            #    print("Connecting to Elasticsearch Cloud...")
            #    return Elasticsearch(hosts=[es_url],
            #    api_key=es_api_key,
            #    verify_certs=True,
            #    request_timeout=30)
            #else:
            #    print(f"Connecting to Elasticsearch at {args.es_host}:{args.es_port}...")
            #    es = Elasticsearch([{'host': args.es_host, 'port': args.es_port, 'scheme': 'http'}])
        
        # Create indices
        create_index(es, 'app_users', schemas['users'])
        create_index(es, 'reservations', schemas['reservations'])
        create_index(es, 'room_availability', schemas['room_availability'])
        
        # Index documents
        index_documents(es, 'app_users', SAMPLE_USERS)
        index_documents(es, 'reservations', all_reservations)
        index_documents(es, 'room_availability', room_availability)
        
        print("User data loading complete!")


def delete_user_indices(es_client, indices=None):
    """Delete user-related Elasticsearch indices."""
    if indices is None:
        indices = ['app_users', 'reservations', 'room_availability']
    
    for index_name in indices:
        try:
            if es_client.indices.exists(index=index_name):
                es_client.indices.delete(index=index_name)
                print(f"Deleted index: {index_name}")
            else:
                print(f"Index {index_name} does not exist. Skipping deletion.")
        except Exception as e:
            print(f"Error deleting index {index_name}: {e}")

if __name__ == "__main__":
    main()
