import asyncio
import sys
from typing import Dict, List, Any, Optional
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
import os
import uuid
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# to interact with MCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# to interact with Amazon Bedrock
import boto3
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError

# to interact with Elasticsearch directly
from elasticsearch import Elasticsearch, helpers, exceptions

# Constants
MAX_TOKENS = 4096
MAX_TURNS = 15

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
# Travel Advisory System Prompt

You are a travel advisory assistant that helps users find information about destinations, attractions, hotels, travel advisories, weather forecasts, and events. You have access to Elasticsearch through an MCP server to retrieve relevant information. You can also help users manage their hotel reservations and view their booking history.
Current date is 9th March 2026.

## Logged-In User
The currently logged-in user is **Varun Jasti** (user_id: USER_VJASTI). 
- Loyalty tier: Platinum, 15,000 points
- Preferred currency: USD
- You do NOT need to ask for the user's name or personal details — they are already known.
- When the user wants to book a room, the ONLY thing you need to ask for is their **email address** to send the confirmation.

## Booking Flow
When a user wants to book a hotel room:
1. Confirm the hotel name, room type, check-in date, and check-out date (gather from conversation context if already discussed).
2. Ask for the user's **email address** for the booking confirmation.
3. Before booking, confirm the details with the user and mention that the **card on file** will be used for payment.
4. Once you have all details and the user confirms, call the `book_room` tool to create the reservation. This tool checks availability, creates the reservation in Elasticsearch, and decrements room availability automatically.
4. After a successful booking, use the AWS SES MCP `send-email` tool to send a confirmation email. IMPORTANT: Only pass `to`, `subject`, and `text` parameters. Do NOT pass `from`, `replyTo`, `cc`, or `bcc` — the sender is pre-configured on the server.
5. If the booking fails (no availability), inform the user and suggest alternatives.

## Reservation Management
- `book_room`: Create a new reservation (checks availability, updates ES)
- `view_reservation`: View reservation details by ID
- `cancel_reservation`: Cancel a reservation (restores room availability in ES)
- `list_my_reservations`: List all reservations for the current user

## CRITICAL: Weather Queries
When the user asks about weather, forecasts, or climate conditions for any location:
1. For **US locations only**: Call the `get_forecast` MCP tool using the destination's latitude and longitude. Also call `get_alerts` with the state code to check for active weather alerts.
2. For **non-US locations** (e.g., Paris, Tokyo, Bali): Use the Elasticsearch `weather` index directly — the NWS weather API only covers the United States.
3. You can find latitude/longitude for destinations in the destinations index or use well-known coordinates.

## Available Elasticsearch Indices

### 1. Destinations Index
This index contains information about travel destinations around the world.

**Key fields:**
- `destination_id`: Unique identifier for the destination
- `name`: Name of the destination (typically City, Country)
- `city`: City name
- `country`: Country name
- `continent`: Continent name
- `description`: Detailed description of the destination
- `best_season`: Best time of year to visit
- `climate`: Climate type (Tropical, Dry, Temperate, etc.)
- `language`: Primary language spoken
- `currency`: Local currency code
- `safety_rating`: Safety rating on a scale of 1-10
- `popularity_score`: Popularity score on a scale of 1-100
- `cost_level`: Budget, Moderate, or Luxury
- `tags`: Keywords describing the destination (Beach, Mountain, Cultural, etc.)

**Example queries:**
- Find destinations in Europe with beaches
- Find budget-friendly destinations in Asia
- Find destinations with high safety ratings

### 2. Attractions Index
This index contains information about tourist attractions at various destinations.

**Key fields:**
- `attraction_id`: Unique identifier for the attraction
- `destination_id`: Reference to the destination
- `name`: Name of the attraction
- `type`: Type of attraction (Museum, Park, Monument, etc.)
- `description`: Detailed description of the attraction
- `opening_hours`: Opening time
- `closing_hours`: Closing time
- `price_range`: Cost indicator (Free, $, $$, $$$)
- `duration_minutes`: Typical visit duration in minutes
- `rating`: User rating on a scale of 0-5
- `tags`: Keywords describing the attraction
- `best_time_to_visit`: Recommended time of day to visit
- `crowd_level`: Expected crowd level (Low, Moderate, High)

**Example queries:**
- Find free museums in Paris
- Find family-friendly attractions in Tokyo
- Find highly-rated historical sites in Rome

### 3. Hotels Index
This index contains information about hotels and accommodations.

**Key fields:**
- `hotel_id`: Unique identifier for the hotel
- `destination_id`: Reference to the destination
- `name`: Name of the hotel
- `brand`: Hotel chain or brand
- `star_rating`: Official star rating (1-5)
- `user_rating`: User rating on a scale of 0-5
- `price_per_night`: Average price per night
- `currency`: Currency for the price
- `amenities`: Available amenities (Pool, Spa, Gym, etc.)
- `room_types`: Available room types
- `breakfast_included`: Whether breakfast is included
- `free_wifi`: Whether free WiFi is available
- `distance_to_center_km`: Distance to city center in kilometers

**Example queries:**
- Find 4-star hotels in Barcelona with a pool
- Find budget hotels near the city center in New York
- Find family-friendly accommodations in Orlando

### 4. Advisories Index
This index contains travel advisories and safety information.

**Key fields:**
- `advisory_id`: Unique identifier for the advisory
- `destination_id`: Reference to the destination
- `country`: Country name
- `advisory_level`: Risk level (Low, Medium, High, Extreme)
- `description`: Description of the advisory
- `issue_date`: Date the advisory was issued
- `expiry_date`: Date the advisory expires
- `issuing_authority`: Organization that issued the advisory
- `health_risks`: Health-related risks
- `safety_risks`: Safety-related risks
- `entry_requirements`: Requirements for entering the country
- `visa_required`: Whether a visa is required
- `vaccination_required`: Required vaccinations

**Example queries:**
- Check current travel advisories for Thailand
- Find countries with low safety risks
- Check visa requirements for Japan

### 5. Weather Index
This index contains weather forecasts for all destinations. Use this index for non-US locations. For US locations, prefer the `get_forecast` and `get_alerts` MCP tools first, then fall back to this index if needed.

**Key fields:**
- `weather_id`: Unique identifier for the weather record
- `destination_id`: Reference to the destination
- `date`: Date of the forecast
- `temperature_high_celsius`: High temperature in Celsius
- `temperature_low_celsius`: Low temperature in Celsius
- `precipitation_mm`: Expected precipitation in millimeters
- `humidity_percent`: Humidity percentage
- `weather_condition`: Weather condition (Sunny, Cloudy, Rainy, etc.)
- `uv_index`: UV index

**Example queries:**
- Check the weather forecast for London next week
- Find destinations with warm weather in December
- Check if it will rain in Tokyo during my trip

### 6. Events Index
This index contains information about events happening at destinations.

**Key fields:**
- `event_id`: Unique identifier for the event
- `destination_id`: Reference to the destination
- `name`: Name of the event
- `type`: Type of event (Festival, Concert, Sports, etc.)
- `description`: Description of the event
- `start_date`: Start date of the event
- `end_date`: End date of the event
- `venue`: Event venue
- `price_range`: Cost indicator (Free, $, $$, $$$)
- `ticket_required`: Whether tickets are required
- `local_significance`: Significance level (Low, Medium, High)

VERY IMPORTANT: Use `name` when searching directly for events in Elasticsearch queries. Only when you run co-related table queries use `event_id` or `destination_id` in searches.
**Example queries:**
- Find festivals in Barcelona in July
- Find free events in New York this weekend
- Find major cultural events in Japan next month

### 7. Users Index
This index contains user profile information.

**Key fields:**
- `user_id`: Unique identifier for the user
- `email`: User's email address
- `first_name`: User's first name
- `last_name`: User's last name
- `phone`: User's phone number
- `date_of_birth`: User's date of birth
- `nationality`: User's nationality
- `preferred_language`: User's preferred language
- `preferred_currency`: User's preferred currency
- `loyalty_tier`: Loyalty program tier (Standard, Silver, Gold, Platinum)
- `loyalty_points`: Accumulated loyalty points
- `preferences`: User's room and stay preferences
- `dietary_restrictions`: User's dietary restrictions
- `special_needs`: Any special needs or accessibility requirements

**Example queries:**
- Find user profile by email
- Get user's loyalty status
- Check user's preferences

### 8. Reservations Index
This index contains hotel reservation information.

**Key fields:**
- `reservation_id`: Unique identifier for the reservation
- `user_id`: Reference to the user
- `hotel_id`: Reference to the hotel
- `room_type`: Type of room booked
- `check_in_date`: Check-in date
- `check_out_date`: Check-out date
- `num_guests`: Number of guests
- `num_rooms`: Number of rooms
- `total_price`: Total price for the stay
- `currency`: Currency for the price
- `payment_status`: Status of payment (Pending, Paid, Refunded, etc.)
- `booking_date`: Date when the booking was made
- `status`: Reservation status (Confirmed, Cancelled, Completed, etc.)
- `special_requests`: Any special requests for the stay
- `confirmation_code`: Confirmation code for the reservation

**Example queries:**
- Find user's upcoming reservations
- Check reservation details by confirmation code
- Get user's past stays at a hotel

### 9. Room Availability Index
This index contains information about room availability at hotels.

**Key fields:**
- `availability_id`: Unique identifier for the availability record
- `hotel_id`: Reference to the hotel
- `hotel_name`: Full name of the hotel
- `city`: City where the hotel is located
- `room_type`: Type of room (Standard, Deluxe, Suite)
- `date`: Date for which availability is recorded
- `available_rooms`: Number of available rooms
- `total_rooms`: Total number of rooms of this type
- `price`: Price for the room on this date
- `currency`: Currency for the price
- `promotion_code`: Promotion code if applicable
- `discount_percentage`: Discount percentage if applicable
- `minimum_stay`: Minimum number of nights required
- `is_closed`: Whether the hotel is closed on this date

You can search room_availability directly by `hotel_name` and `city` — no need to cross-reference the hotels index.
When the user asks for more hotel details (amenities, star rating, distance to center, etc.), query the `hotels` index using the `hotel_id` from room_availability. Use a `term` query on `hotel_id.keyword` for exact matching.
**Example queries:**
- Check room availability in Paris for next weekend
- Find hotels with available rooms for a specific date range
- Get pricing for a deluxe room at a specific hotel

## Query Guidelines

When a user asks a question:

1. Identify which index or indices are most relevant to the query
2. Formulate appropriate Elasticsearch queries to retrieve the information
3. Present the information in a clear, concise manner
4. For complex queries that span multiple indices, use multiple queries and join the results
5. If weather information is requested, use both the Elasticsearch MCP server and the Weather MCP server as appropriate
6. Always provide context about the source and recency of the information
7. When sorting or filtering on string fields, use the `.keyword` sub-field (e.g. `city.keyword`, `room_type.keyword`, `hotel_id.keyword`). The only exceptions are `name`, `description`, `address`, `venue`, `special_needs`, `special_requests`, `health_risks`, `safety_risks`, `entry_requirements`, `currency_restrictions`, `local_laws`, `emergency_contacts` — these are plain `text` fields with no `.keyword` sub-field.
8. The `queryBody` parameter must be a JSON object, not a string.

## Response Format

Structure your responses to include:

1. Direct answer to the user's question
2. Supporting details from the retrieved data
3. Related information that might be helpful
4. Suggestions for follow-up questions or actions

For hotel reservations or bookings:
- The user is already logged in as Varun Jasti — do NOT ask for name or personal details.
- Only ask for the user's **email address** to send the booking confirmation.
- Use the `book_room` tool to create the reservation. It checks the `room_availability` index, creates the reservation in the `reservations` index, and decrements `available_rooms` automatically.
- After a successful booking, use the AWS SES MCP server to send a confirmation email.
- Use `list_my_reservations` to show the user's bookings from the `reservations` index.
- Use `cancel_reservation` to cancel — it updates the `reservations` index and restores `available_rooms` in `room_availability`.

## Example Interactions

**User:** "I'm planning a trip to Bali next month. What's the weather like and are there any travel advisories?"

**Assistant:** *[Uses Elasticsearch to query the weather and advisories indices for Bali]*

"Bali is expected to have average temperatures between 24-31°C next month with occasional afternoon showers. The current travel advisory level is Low, with some precautions recommended for certain areas. The Indonesian government requires a visa on arrival for most visitors, and it's recommended to have travel insurance that covers medical evacuation. Popular activities during this season include visiting temples, rice terraces, and beaches, though some beach areas may have stronger currents this time of year."

**User:** "Can you recommend some hotels in Paris with a view of the Eiffel Tower?"

**Assistant:** *[Uses Elasticsearch to query the hotels index for Paris hotels, possibly filtering by location or amenities]*

"I found several hotels in Paris with views of the Eiffel Tower:

1. Hotel Le Meurice (5-star) - $450/night, exceptional 4.8/5 rating
2. Shangri-La Hotel (5-star) - $520/night, with 4.7/5 rating
3. Hotel Balzac (4-star) - $320/night, with 4.3/5 rating
4. Citadines Tour Eiffel (3-star) - $210/night, with 4.0/5 rating

Would you like more details about any of these hotels or help with booking?"

**User:** "Book a Deluxe room at The Ritz Paris from March 15 to March 20"

**Assistant:** "I'd be happy to book that for you, Varun! I just need your email address to send the confirmation."

**User:** "varun@example.com"

**Assistant:** *[Calls book_room tool → checks room_availability index → creates reservation in reservations index → decrements available_rooms]*

"Your reservation is confirmed!

Confirmation Code: CONF8A3B2E
Hotel: The Ritz Paris
Room: Deluxe
Check-in: March 15, 2026
Check-out: March 20, 2026
Total: €3,750.00
Status: Confirmed

I'll send a confirmation email to varun@example.com now."

**User:** "Show me my reservations"

**Assistant:** *[Calls list_my_reservations tool → queries reservations index for USER_VJASTI]*

Once you provide these details, I can search for available hotels that match your criteria."

"""


@dataclass
class Message:
    """Helper class for constructing Bedrock Converse API messages."""
    role: str
    content: List[Dict[str, Any]]

    @classmethod
    def user(cls, text: str) -> 'Message':
        return cls(role="user", content=[{"text": text}])

    @classmethod
    def assistant(cls, text: str) -> 'Message':
        return cls(role="assistant", content=[{"text": text}])

    @classmethod
    def assistant_tool_use(cls, tool_use_id: str, name: str, input_data: dict) -> 'Message':
        return cls(
            role="assistant",
            content=[{
                "toolUse": {
                    "toolUseId": tool_use_id,
                    "name": name,
                    "input": input_data
                }
            }]
        )

    @classmethod
    def user_tool_result(cls, tool_use_id: str, content: List[Dict], status: str = "success") -> 'Message':
        return cls(
            role="user",
            content=[{
                "toolResult": {
                    "toolUseId": tool_use_id,
                    "content": content,
                    "status": status
                }
            }]
        )

    @staticmethod
    def format_tools_for_bedrock(tools_list: List[Dict]) -> List[Dict]:
        """Convert MCP tool definitions to Bedrock Converse toolConfig format."""
        bedrock_tools = []
        for tool in tools_list:
            properties = tool["input_schema"].get("properties", {})
            required = tool["input_schema"].get("required", [])

            # Ensure at least one required field if properties exist
            if not required and properties:
                required = [next(iter(properties))]

            bedrock_tools.append({
                "toolSpec": {
                    "name": tool["name"],
                    "description": tool.get("description", ""),
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": properties,
                            "required": required
                        }
                    }
                }
            })
        return bedrock_tools


class HotelReservationManager:
    """Manages hotel reservations in Elasticsearch with real availability updates."""

    # Hardcoded logged-in user
    CURRENT_USER = {
        "user_id": "USER_VJASTI",
        "first_name": "Varun",
        "last_name": "Jasti",
        "phone": "+1-555-987-6543",
        "nationality": "United States",
        "preferred_language": "English",
        "preferred_currency": "USD",
        "loyalty_tier": "Platinum",
        "loyalty_points": 15000,
    }

    def __init__(self, es_client: Elasticsearch):
        self.es = es_client

    def get_current_user(self) -> Dict:
        """Return the hardcoded logged-in user profile."""
        return dict(self.CURRENT_USER)

    # ------------------------------------------------------------------
    # Room availability helpers
    # ------------------------------------------------------------------
    async def check_availability(
        self, hotel_name: str, room_type: str, check_in: str, check_out: str
    ) -> Dict:
        """Check room availability for a hotel across a date range.
        
        Returns dict with 'available' bool, 'dates' list of per-day info,
        'total_price', and 'currency'.
        """
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"hotel_name": hotel_name}},
                        {"term": {"room_type.keyword": room_type}},
                        {"range": {"date": {"gte": check_in, "lt": check_out}}},
                        {"term": {"is_closed": False}},
                    ]
                }
            },
            "sort": [{"date": "asc"}],
            "size": 100,
        }
        try:
            resp = self.es.search(
                index="room_availability",
                query=query["query"],
                sort=query["sort"],
                size=query["size"],
            )
            hits = [h["_source"] for h in resp["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Availability check failed: {e}")
            return {"available": False, "error": str(e)}

        if not hits:
            return {"available": False, "reason": "No availability records found for the given criteria."}

        all_available = all(h.get("available_rooms", 0) > 0 for h in hits)
        total_price = sum(h.get("price", 0) for h in hits)
        currency = hits[0].get("currency", "USD") if hits else "USD"
        hotel_id = hits[0].get("hotel_id", "") if hits else ""
        city = hits[0].get("city", "") if hits else ""

        return {
            "available": all_available,
            "dates": hits,
            "total_price": round(total_price, 2),
            "currency": currency,
            "nights": len(hits),
            "hotel_id": hotel_id,
            "city": city,
            "hotel_name": hits[0].get("hotel_name", hotel_name) if hits else hotel_name,
        }

    async def _decrement_availability(
        self, hotel_name: str, room_type: str, check_in: str, check_out: str
    ) -> bool:
        """Decrement available_rooms by 1 for each night in the booking range."""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"hotel_name": hotel_name}},
                        {"term": {"room_type.keyword": room_type}},
                        {"range": {"date": {"gte": check_in, "lt": check_out}}},
                    ]
                }
            },
            "size": 100,
        }
        try:
            resp = self.es.search(
                index="room_availability",
                query=query["query"],
                size=query["size"],
            )
            for hit in resp["hits"]["hits"]:
                doc_id = hit["_id"]
                current_avail = hit["_source"].get("available_rooms", 0)
                new_avail = max(0, current_avail - 1)
                self.es.update(
                    index="room_availability",
                    id=doc_id,
                    doc={"available_rooms": new_avail},
                    refresh=True,
                )
            return True
        except Exception as e:
            logger.error(f"Failed to decrement availability: {e}")
            return False

    async def _restore_availability(
        self, hotel_name: str, room_type: str, check_in: str, check_out: str
    ) -> bool:
        """Restore available_rooms by 1 for each night (used on cancellation)."""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"hotel_name": hotel_name}},
                        {"term": {"room_type.keyword": room_type}},
                        {"range": {"date": {"gte": check_in, "lt": check_out}}},
                    ]
                }
            },
            "size": 100,
        }
        try:
            resp = self.es.search(
                index="room_availability",
                query=query["query"],
                size=query["size"],
            )
            for hit in resp["hits"]["hits"]:
                doc_id = hit["_id"]
                src = hit["_source"]
                current_avail = src.get("available_rooms", 0)
                total = src.get("total_rooms", current_avail + 1)
                new_avail = min(total, current_avail + 1)
                self.es.update(
                    index="room_availability",
                    id=doc_id,
                    doc={"available_rooms": new_avail},
                    refresh=True,
                )
            return True
        except Exception as e:
            logger.error(f"Failed to restore availability: {e}")
            return False

    # ------------------------------------------------------------------
    # Reservation CRUD
    # ------------------------------------------------------------------
    async def create_reservation(self, booking: Dict) -> Dict:
        """Create a reservation after verifying availability and updating room counts."""
        hotel_name = booking.get("hotel_name", "Unknown Hotel")
        room_type = booking.get("room_type", "Standard")
        check_in = booking.get("check_in_date")
        check_out = booking.get("check_out_date")
        email = booking.get("email", "")

        # 1. Verify availability
        avail = await self.check_availability(hotel_name, room_type, check_in, check_out)
        if not avail.get("available"):
            reason = avail.get("reason", "Rooms not available for one or more nights in the requested range.")
            return {"error": reason}

        # 2. Build reservation document
        reservation_id = str(uuid.uuid4())
        confirmation_code = f"CONF{uuid.uuid4().hex[:6].upper()}"
        now_iso = datetime.now().isoformat()

        reservation = {
            "reservation_id": reservation_id,
            "confirmation_code": confirmation_code,
            "user_id": self.CURRENT_USER["user_id"],
            "user_name": f"{self.CURRENT_USER['first_name']} {self.CURRENT_USER['last_name']}",
            "user_email": email,
            "hotel_name": avail.get("hotel_name", hotel_name),
            "hotel_id": avail.get("hotel_id", ""),
            "city": avail.get("city", ""),
            "room_type": room_type,
            "check_in_date": check_in,
            "check_out_date": check_out,
            "num_guests": booking.get("num_guests", 1),
            "num_rooms": 1,
            "total_price": avail["total_price"],
            "currency": avail["currency"],
            "nights": avail.get("nights", 0),
            "payment_status": "Paid",
            "payment_method": "Credit Card",
            "booking_date": now_iso,
            "booking_source": "Direct",
            "status": "Confirmed",
            "special_requests": booking.get("special_requests", ""),
            "breakfast_included": booking.get("breakfast_included", False),
            "is_refundable": True,
            "cancellation_deadline": check_in,
            "created_at": now_iso,
            "updated_at": now_iso,
        }

        # 3. Index the reservation
        try:
            logger.info(f"Indexing reservation {reservation_id} with special_requests='{reservation.get('special_requests', '')}'")
            resp = self.es.index(
                index="reservations", id=reservation_id, document=reservation, refresh=True
            )
            if resp["result"] != "created":
                return {"error": f"Elasticsearch returned: {resp['result']}"}
        except Exception as e:
            return {"error": str(e)}

        # 4. Decrement room availability
        await self._decrement_availability(hotel_name, room_type, check_in, check_out)

        return reservation

    async def get_reservation(self, reservation_id: str) -> Optional[Dict]:
        """Get a reservation by ID."""
        try:
            resp = self.es.get(index="reservations", id=reservation_id)
            return resp["_source"]
        except exceptions.NotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error retrieving reservation {reservation_id}: {e}")
            return None

    async def update_reservation(self, reservation_id: str, update_data: Dict) -> Optional[Dict]:
        """Update fields on an existing reservation, handling date/room changes with availability updates."""
        current = await self.get_reservation(reservation_id)
        if not current:
            return None

        # Guard: don't allow updates on cancelled reservations
        if current.get("status") == "Cancelled":
            return {"error": "Cannot update a cancelled reservation."}

        old_hotel = current.get("hotel_name", "")
        old_room = current.get("room_type", "")
        old_checkin = current.get("check_in_date", "")
        old_checkout = current.get("check_out_date", "")

        # Apply updates
        for k, v in update_data.items():
            current[k] = v
        current["updated_at"] = datetime.now().isoformat()

        new_hotel = current.get("hotel_name", old_hotel)
        new_room = current.get("room_type", old_room)
        new_checkin = current.get("check_in_date", old_checkin)
        new_checkout = current.get("check_out_date", old_checkout)

        dates_changed = (old_hotel != new_hotel or old_room != new_room
                         or old_checkin != new_checkin or old_checkout != new_checkout)

        # If dates/hotel/room changed, verify new availability first
        if dates_changed:
            avail = await self.check_availability(new_hotel, new_room, new_checkin, new_checkout)
            if not avail.get("available"):
                return {"error": avail.get("reason", "New dates/room not available.")}
            # Update price and hotel details from new availability
            current["total_price"] = avail["total_price"]
            current["currency"] = avail["currency"]
            current["nights"] = avail.get("nights", 0)
            current["hotel_id"] = avail.get("hotel_id", current.get("hotel_id", ""))
            current["city"] = avail.get("city", current.get("city", ""))
            current["hotel_name"] = avail.get("hotel_name", new_hotel)

        try:
            self.es.index(index="reservations", id=reservation_id, document=current, refresh=True)
        except Exception as e:
            logger.error(f"Error updating reservation: {e}")
            return None

        # If dates changed, restore old availability and decrement new
        if dates_changed:
            await self._restore_availability(old_hotel, old_room, old_checkin, old_checkout)
            await self._decrement_availability(new_hotel, new_room, new_checkin, new_checkout)

        return current

    async def cancel_reservation(self, reservation_id: str) -> Optional[Dict]:
        """Cancel a reservation and restore room availability."""
        current = await self.get_reservation(reservation_id)
        if not current:
            return None

        # Guard: don't cancel an already-cancelled reservation (would double-restore availability)
        if current.get("status") == "Cancelled":
            return {"error": "This reservation is already cancelled."}

        current["status"] = "Cancelled"
        current["payment_status"] = "Refunded"
        current["updated_at"] = datetime.now().isoformat()
        try:
            self.es.index(index="reservations", id=reservation_id, document=current, refresh=True)
            # Restore availability
            await self._restore_availability(
                current.get("hotel_name", ""),
                current.get("room_type", ""),
                current.get("check_in_date", ""),
                current.get("check_out_date", ""),
            )
            return current
        except Exception as e:
            logger.error(f"Error cancelling reservation: {e}")
            return None

    async def list_user_reservations(self) -> List[Dict]:
        """List all reservations for the current logged-in user."""
        query = {
            "query": {"term": {"user_id": self.CURRENT_USER["user_id"]}},
            "sort": [{"created_at": {"order": "desc"}}],
            "size": 50,
        }
        try:
            resp = self.es.search(
                index="reservations",
                query=query["query"],
                sort=query["sort"],
                size=query["size"],
            )
            return [h["_source"] for h in resp["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Error listing reservations: {e}")
            return []


class MultiServerMCPClient:
    MODEL_ID = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
    
    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        
        # Initialize Bedrock client with retry config
        self.bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            config=BotoConfig(
                retries={"max_attempts": 3, "mode": "adaptive"},
                read_timeout=120,
                connect_timeout=10
            )
        )
        
        self.all_tools = {}
        self.server_configs = {}
        self.tool_to_server: Dict[str, str] = {}  # tool_name -> server_name mapping
        
        # Initialize Elasticsearch client
        es_url = os.getenv("ES_URL")
        es_api_key = os.getenv("ES_API_KEY")
        
        if not es_url or not es_api_key:
            raise ValueError("ES_URL and ES_API_KEY must be set in the .env file")
        
        self.es = Elasticsearch(
            hosts=[es_url],
            api_key=es_api_key
        )
        
        # Initialize the reservation manager
        self.reservation_manager = HotelReservationManager(self.es)
        
        # Conversation history for multi-turn context
        self.conversation_history: List[Dict] = []
        self.max_history_turns = 20  # Keep last N user/assistant pairs to avoid token limits

    async def connect_to_servers(self, server_configs: Dict[str, Dict]):
        """Connect to multiple MCP servers"""
        self.server_configs = server_configs
        for server_name, config in server_configs.items():
            await self.connect_to_server(server_name, config)
        
        print(f"\nConnected to {len(self.sessions)} servers with {sum(len(t) for t in self.all_tools.values())} total tools")
        for server, tools in self.all_tools.items():
            print(f"- {server}: {[tool.name for tool in tools]}")

    async def connect_to_server(self, server_name: str, config: Dict):
        """Connect to an MCP server using the provided configuration"""
        if "command" not in config:
            raise ValueError(f"Invalid server configuration for {server_name}: missing 'command'")

        server_params = StdioServerParameters(
            command=config["command"],
            args=config.get("args", []),
            env=config.get("env", None)
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await session.initialize()

        response = await session.list_tools()
        print(f"\nConnected to {server_name} with tools:", [tool.name for tool in response.tools])
        
        self.sessions[server_name] = session
        self.all_tools[server_name] = response.tools
        
        # Build tool-to-server mapping
        for tool in response.tools:
            self.tool_to_server[tool.name] = server_name

    def _get_available_tools(self) -> tuple[List[Dict], List[Dict]]:
        """Build the available tools list and Bedrock-formatted tools."""
        available_tools = []
        for server_name, tools in self.all_tools.items():
            for tool in tools:
                tool_info = {
                    "name": tool.name,
                    "server": server_name,
                    "description": tool.description or "",
                    "input_schema": tool.inputSchema or {"type": "object", "properties": {}}
                }
                available_tools.append(tool_info)

        bedrock_tools = Message.format_tools_for_bedrock(available_tools)
        return available_tools, bedrock_tools

    def _converse_stream(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Make a Bedrock ConverseStream API call and return the event stream."""
        try:
            kwargs = {
                "modelId": self.MODEL_ID,
                "system": [{"text": SYSTEM_PROMPT}],
                "messages": messages,
                "inferenceConfig": {
                    "maxTokens": MAX_TOKENS,
                    "temperature": 0.7,
                },
            }
            
            # Only include toolConfig if tools are available
            if tools:
                kwargs["toolConfig"] = {"tools": tools}
            
            response = self.bedrock.converse_stream(**kwargs)
            return response
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_msg = e.response['Error']['Message']
            logger.error(f"Bedrock API error ({error_code}): {error_msg}")
            raise

    def _collect_stream(self, response: Dict, print_text: bool = True) -> tuple[List[Dict], str]:
        """Consume a ConverseStream response, optionally printing text tokens in real-time.
        
        Returns (content_blocks, stop_reason) where content_blocks is the reconstructed
        list of content items (text and toolUse) matching the non-streaming format.
        """
        content_blocks = []
        stop_reason = ""
        
        # State for accumulating the current block
        current_text = ""
        current_tool_use = None
        tool_input_json = ""
        
        stream = response.get("stream")
        if not stream:
            return content_blocks, "end_turn"
        
        for event in stream:
            if "contentBlockStart" in event:
                start = event["contentBlockStart"].get("start", {})
                if "toolUse" in start:
                    # Flush any accumulated text
                    if current_text:
                        content_blocks.append({"text": current_text})
                        current_text = ""
                    current_tool_use = {
                        "toolUseId": start["toolUse"]["toolUseId"],
                        "name": start["toolUse"]["name"],
                    }
                    tool_input_json = ""
                    
            elif "contentBlockDelta" in event:
                delta = event["contentBlockDelta"].get("delta", {})
                if "text" in delta:
                    chunk = delta["text"]
                    current_text += chunk
                    if print_text:
                        print(chunk, end="", flush=True)
                elif "toolUse" in delta:
                    tool_input_json += delta["toolUse"].get("input", "")
                    
            elif "contentBlockStop" in event:
                if current_tool_use is not None:
                    # Parse accumulated JSON input
                    try:
                        parsed_input = json.loads(tool_input_json) if tool_input_json else {}
                    except json.JSONDecodeError:
                        parsed_input = {}
                    current_tool_use["input"] = parsed_input
                    content_blocks.append({"toolUse": current_tool_use})
                    current_tool_use = None
                    tool_input_json = ""
                elif current_text:
                    content_blocks.append({"text": current_text})
                    current_text = ""
                    
            elif "messageStop" in event:
                stop_reason = event["messageStop"].get("stopReason", "end_turn")
                
            elif "metadata" in event:
                # Contains usage info; we can log it if needed
                usage = event["metadata"].get("usage", {})
                if usage:
                    logger.debug(f"Token usage - input: {usage.get('inputTokens', 0)}, output: {usage.get('outputTokens', 0)}")
        
        # Flush any remaining text
        if current_text:
            content_blocks.append({"text": current_text})
        
        if print_text:
            print()  # Newline after streaming output
            
        return content_blocks, stop_reason

    async def process_query(self, query: str) -> str:
        # Add user message to conversation history
        user_msg = Message.user(query).__dict__
        self.conversation_history.append(user_msg)
        
        # Build messages from full conversation history
        messages = list(self.conversation_history)
        
        available_tools, bedrock_tools = self._get_available_tools()
        
        # Add reservation management tools
        reservation_tools = self._get_reservation_tools()
        bedrock_tools.extend(reservation_tools)
        
        response = self._converse_stream(messages, bedrock_tools)
        
        result = await self._process_response(response, messages, bedrock_tools)
        
        # After processing, extract the final assistant text and add to history
        assistant_text = result.replace("[Thinking: ", "").strip()
        clean_lines = [
            line for line in assistant_text.split("\n")
            if not line.startswith("[Calling tool ") and not line.startswith("[Tool ") and not line.startswith("[ERROR")
        ]
        clean_text = "\n".join(clean_lines).strip()
        if clean_text:
            self.conversation_history.append(Message.assistant(clean_text).__dict__)
        
        self._trim_history()
        
        return result
    
    def _trim_history(self):
        """Trim conversation history to stay within token limits."""
        # Each turn is a user + assistant pair = 2 messages
        max_messages = self.max_history_turns * 2
        if len(self.conversation_history) > max_messages:
            # Keep the most recent messages, ensuring we start with a user message
            trimmed = self.conversation_history[-max_messages:]
            # Make sure we start with a user message
            while trimmed and trimmed[0]["role"] != "user":
                trimmed.pop(0)
            self.conversation_history = trimmed

    # ------------------------------------------------------------------
    # Reservation tools exposed to the LLM
    # ------------------------------------------------------------------
    RESERVATION_TOOL_NAMES = {"book_room", "view_reservation", "cancel_reservation", "update_reservation", "list_my_reservations"}

    def _get_reservation_tools(self) -> List[Dict]:
        """Return Bedrock-formatted tool specs for reservation management."""
        return [
            {
                "toolSpec": {
                    "name": "book_room",
                    "description": (
                        "Book a hotel room. Checks availability in Elasticsearch, creates the reservation, "
                        "decrements room availability, and stores the reservation in the 'reservations' index. "
                        "The logged-in user is Varun Jasti. You must collect the user's email for confirmation. "
                        "IMPORTANT: If the user mentions ANY special requests (e.g. extra water bottles, late check-in, "
                        "extra pillows, airport shuttle, etc.), you MUST include them in the special_requests parameter."
                    ),
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "hotel_name": {"type": "string", "description": "Full hotel name as it appears in the system"},
                                "room_type": {"type": "string", "description": "Room type: Standard, Deluxe, or Suite"},
                                "check_in_date": {"type": "string", "description": "Check-in date in YYYY-MM-DD format"},
                                "check_out_date": {"type": "string", "description": "Check-out date in YYYY-MM-DD format"},
                                "num_guests": {"type": "integer", "description": "Number of guests"},
                                "email": {"type": "string", "description": "Email address for booking confirmation"},
                                "special_requests": {"type": "string", "description": "Special requests from the user such as extra water bottles, late check-in, extra pillows, airport shuttle, room preferences, etc. Always include if the user mentions any."},
                            },
                            "required": ["hotel_name", "room_type", "check_in_date", "check_out_date", "email"],
                        }
                    },
                }
            },
            {
                "toolSpec": {
                    "name": "view_reservation",
                    "description": "View details of a specific reservation by its reservation ID.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "reservation_id": {"type": "string", "description": "The reservation UUID"},
                            },
                            "required": ["reservation_id"],
                        }
                    },
                }
            },
            {
                "toolSpec": {
                    "name": "cancel_reservation",
                    "description": "Cancel a reservation by ID. This updates the reservation status to Cancelled, sets payment to Refunded, and restores room availability in Elasticsearch. Cannot cancel an already-cancelled reservation.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "reservation_id": {"type": "string", "description": "The reservation UUID to cancel"},
                            },
                            "required": ["reservation_id"],
                        }
                    },
                }
            },
            {
                "toolSpec": {
                    "name": "update_reservation",
                    "description": (
                        "Update an existing reservation. Can change dates, room type, or special requests. "
                        "If dates or room type change, availability is checked, old availability is restored, "
                        "and new availability is decremented in Elasticsearch automatically. "
                        "Cannot update a cancelled reservation. "
                        "IMPORTANT: If the user wants to add or change special requests (e.g. extra water bottles, "
                        "late check-in, extra pillows), include them in the special_requests parameter."
                    ),
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "reservation_id": {"type": "string", "description": "The reservation UUID to update"},
                                "check_in_date": {"type": "string", "description": "New check-in date in YYYY-MM-DD format"},
                                "check_out_date": {"type": "string", "description": "New check-out date in YYYY-MM-DD format"},
                                "room_type": {"type": "string", "description": "New room type: Standard, Deluxe, or Suite"},
                                "hotel_name": {"type": "string", "description": "New hotel name (if changing hotels)"},
                                "num_guests": {"type": "integer", "description": "Updated number of guests"},
                                "special_requests": {"type": "string", "description": "Updated special requests"},
                            },
                            "required": ["reservation_id"],
                        }
                    },
                }
            },
            {
                "toolSpec": {
                    "name": "list_my_reservations",
                    "description": "List all reservations for the currently logged-in user (Varun Jasti).",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {},
                            "required": [],
                        }
                    },
                }
            },
        ]

    async def _execute_reservation_tool(self, tool_name: str, tool_args: Dict) -> str:
        """Execute a local reservation tool and return the result as text."""
        try:
            if tool_name == "book_room":
                result = await self.reservation_manager.create_reservation(tool_args)
                if "error" in result:
                    return json.dumps({"status": "error", "message": result["error"]})
                return json.dumps({
                    "status": "success",
                    "reservation_id": result["reservation_id"],
                    "confirmation_code": result["confirmation_code"],
                    "hotel_name": result["hotel_name"],
                    "hotel_id": result.get("hotel_id", ""),
                    "city": result.get("city", ""),
                    "room_type": result["room_type"],
                    "check_in_date": result["check_in_date"],
                    "check_out_date": result["check_out_date"],
                    "nights": result.get("nights", 0),
                    "num_guests": result.get("num_guests", 1),
                    "total_price": result["total_price"],
                    "currency": result["currency"],
                    "user_name": result["user_name"],
                    "user_email": result["user_email"],
                    "payment_status": result["payment_status"],
                    "booking_status": result["status"],
                    "special_requests": result.get("special_requests", ""),
                    "breakfast_included": result.get("breakfast_included", False),
                })

            elif tool_name == "view_reservation":
                res = await self.reservation_manager.get_reservation(tool_args["reservation_id"])
                if not res:
                    return json.dumps({"status": "error", "message": f"Reservation {tool_args['reservation_id']} not found."})
                return json.dumps({"status": "success", "reservation": res})

            elif tool_name == "cancel_reservation":
                res = await self.reservation_manager.cancel_reservation(tool_args["reservation_id"])
                if not res:
                    return json.dumps({"status": "error", "message": f"Reservation {tool_args['reservation_id']} not found or could not be cancelled."})
                if "error" in res:
                    return json.dumps({"status": "error", "message": res["error"]})
                return json.dumps({"status": "success", "message": "Reservation cancelled and payment refunded. Room availability restored.", "reservation": res})

            elif tool_name == "update_reservation":
                reservation_id = tool_args.get("reservation_id")
                update_fields = {k: v for k, v in tool_args.items() if k != "reservation_id"}
                res = await self.reservation_manager.update_reservation(reservation_id, update_fields)
                if not res:
                    return json.dumps({"status": "error", "message": f"Reservation {reservation_id} not found."})
                if "error" in res:
                    return json.dumps({"status": "error", "message": res["error"]})
                return json.dumps({"status": "success", "message": "Reservation updated successfully.", "reservation": res})

            elif tool_name == "list_my_reservations":
                reservations = await self.reservation_manager.list_user_reservations()
                return json.dumps({"status": "success", "count": len(reservations), "reservations": reservations})

            else:
                return json.dumps({"status": "error", "message": f"Unknown reservation tool: {tool_name}"})

        except Exception as e:
            logger.error(f"Reservation tool {tool_name} failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})

    async def _process_response(
        self, 
        response: Dict, 
        messages: List[Dict], 
        bedrock_tools: List[Dict],
    ) -> str:
        """Process Bedrock streaming response, handling the tool-use agentic loop."""
        final_text = []
        turn_count = 0
        
        try:
            while turn_count < MAX_TURNS:
                content_blocks, stop_reason = self._collect_stream(response, print_text=True)
                
                if stop_reason == 'tool_use':
                    messages.append({"role": "assistant", "content": content_blocks})
                    
                    tool_results_content = []
                    
                    for item in content_blocks:
                        if 'text' in item and item['text']:
                            final_text.append(f"[Thinking: {item['text']}]")
                        
                        elif 'toolUse' in item:
                            tool_info = item['toolUse']
                            tool_name = tool_info['name']
                            
                            # Check if this is a local reservation tool
                            if tool_name in self.RESERVATION_TOOL_NAMES:
                                print(f"\n  🔧 Calling tool: {tool_name} (local: reservations)")
                                tool_args_str = json.dumps(tool_info['input'], indent=2)
                                if len(tool_args_str) > 300:
                                    tool_args_str = tool_args_str[:300] + "..."
                                print(f"     Args: {tool_args_str}")
                                
                                result_text = await self._execute_reservation_tool(
                                    tool_name, tool_info['input']
                                )
                                preview = result_text[:150].replace('\n', ' ')
                                print(f"     ✅ Result: {preview}{'...' if len(result_text) > 150 else ''}")
                                
                                tool_results_content.append({
                                    "toolResult": {
                                        "toolUseId": tool_info['toolUseId'],
                                        "content": [{"text": result_text}],
                                        "status": "success"
                                    }
                                })
                                final_text.append(f"[Tool {tool_name} returned: {result_text[:200]}]")
                                continue
                            
                            # Otherwise route to MCP server
                            server_name = self.tool_to_server.get(tool_name)
                            if not server_name:
                                err_msg = f"  ❌ Tool '{tool_name}' not found in any connected server"
                                print(err_msg)
                                tool_results_content.append({
                                    "toolResult": {
                                        "toolUseId": tool_info['toolUseId'],
                                        "content": [{"text": f"Error: Tool {tool_name} not found in any connected server"}],
                                        "status": "error"
                                    }
                                })
                                final_text.append(err_msg)
                                continue
                            
                            print(f"\n  🔧 Calling tool: {tool_name} (server: {server_name})")
                            tool_args_str = json.dumps(tool_info['input'], indent=2)
                            if len(tool_args_str) > 300:
                                tool_args_str = tool_args_str[:300] + "..."
                            print(f"     Args: {tool_args_str}")
                            
                            result_content, display_text = await self._handle_tool_call(
                                server_name, tool_info
                            )
                            tool_results_content.append({
                                "toolResult": {
                                    "toolUseId": tool_info['toolUseId'],
                                    "content": result_content,
                                    "status": "success"
                                }
                            })
                            final_text.extend(display_text)
                    
                    if tool_results_content:
                        messages.append({"role": "user", "content": tool_results_content})
                    
                    response = self._converse_stream(messages, bedrock_tools)
                    turn_count += 1
                    
                elif stop_reason == 'end_turn':
                    for item in content_blocks:
                        if 'text' in item and item['text']:
                            final_text.append(item['text'])
                    return "\n".join(final_text)
                
                else:
                    for item in content_blocks:
                        if 'text' in item and item['text']:
                            final_text.append(item['text'])
                    if stop_reason == 'max_tokens':
                        final_text.append("\n[Response truncated due to token limit]")
                    return "\n".join(final_text)

            if turn_count >= MAX_TURNS:
                final_text.append("\n[Maximum conversation turns reached.]")
                
            return "\n".join(final_text)
            
        except Exception as e:
            import traceback
            logger.error(f"Error processing response: {e}")
            final_text.append(f"\n[Error processing response: {str(e)}]")
            final_text.append(traceback.format_exc())
            return "\n".join(final_text)

    async def _handle_tool_call(
        self, 
        server_name: str, 
        tool_info: Dict, 
    ) -> tuple[List[Dict], List[str]]:
        """Execute a tool call via MCP and return (result_content, display_text)."""
        tool_name = tool_info['name']
        tool_args = tool_info['input']

        # Fix stringified JSON values — the LLM sometimes serializes nested objects/arrays as strings
        for key, value in tool_args.items():
            if isinstance(value, str):
                stripped = value.strip()
                if stripped.startswith('{') or stripped.startswith('['):
                    try:
                        tool_args[key] = json.loads(stripped)
                    except (json.JSONDecodeError, ValueError):
                        pass

        session = self.sessions[server_name]
        
        display_text = [f"[Calling tool {tool_name} on server {server_name} with args {tool_args}]"]
        
        try:
            result = await session.call_tool(tool_name, tool_args)
            
            # Build tool result content for Bedrock
            result_content = []
            for content in result.content:
                if hasattr(content, 'text') and content.text:
                    result_content.append({"text": content.text})
                elif hasattr(content, 'data'):
                    result_content.append({"json": content.data})
            
            # Ensure we always have content
            if not result_content:
                result_content = [{"text": "Tool executed successfully with no output"}]
            
            # Build display text
            first_text = next((c.text for c in result.content if hasattr(c, 'text') and c.text), "No content")
            display_text.append(f"[Tool {tool_name} returned: {first_text[:200]}]")
            
            # Print result status to console
            preview = first_text[:150].replace('\n', ' ')
            print(f"     ✅ Result: {preview}{'...' if len(first_text) > 150 else ''}")
            
            return result_content, display_text
            
        except Exception as e:
            logger.error(f"Tool call failed: {tool_name} - {e}")
            error_content = [{"text": f"Tool execution failed: {str(e)}"}]
            display_text.append(f"[Tool {tool_name} failed: {str(e)}]")
            print(f"     ❌ Failed: {str(e)}")
            return error_content, display_text

    async def chat_loop(self):
        user = HotelReservationManager.CURRENT_USER
        print(f"\nWelcome to the Travel Advisory System, {user['first_name']} {user['last_name']}!")
        print(f"Loyalty: {user['loyalty_tier']} ({user['loyalty_points']:,} points)")
        print("Type 'quit' to exit, 'new chat' to start a fresh conversation.\n")
        print("Here's what I can help with:")
        print("  🌍 Destination info   — weather, attractions, events, travel advisories")
        print("  🏨 Hotel search       — find and compare hotels at any destination")
        print("  📅 Room booking       — check availability, book, and manage reservations")
        print("  📧 Confirmations      — email booking confirmations via AWS SES")
        print("  📋 My reservations    — view, update, or cancel your bookings")
        
        while True:
            try:
                query = input("\nYou: ").strip()
                if not query:
                    continue
                if query.lower() == 'quit':
                    break
                if query.lower() == 'new chat':
                    self.conversation_history.clear()
                    print("\n🔄 Conversation history cleared. Starting fresh!")
                    continue
                
                print("\nAssistant: ", end="", flush=True)
                await self.process_query(query)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")
                import traceback
                traceback.print_exc()

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Usage: python multi_server_client.py <weather_server_script>")
        sys.exit(1)

    weather_script = sys.argv[1]
    
    es_url = os.getenv("ES_URL")
    es_api_key = os.getenv("ES_API_KEY")

    if not es_url or not es_api_key:
        print("Error: ES_URL and ES_API_KEY must be set in the .env file")
        sys.exit(1)

    # Get AWS SES MCP configuration from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-west-2")
    sender_email = os.getenv("SENDER_EMAIL_ADDRESS")
    reply_to_email = os.getenv("REPLY_TO_EMAIL_ADDRESSES")
    aws_ses_mcp_server_path=os.getenv("AWS_SES_MCP_SERVER_PATH")
    
    # Validate required environment variables
    if not all([aws_access_key_id, aws_secret_access_key, sender_email]):
        print("Error: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and SENDER_EMAIL_ADDRESS must be set in the .env file")
        sys.exit(1)
    
    server_configs = {
        "weather": {
            "command": "python",
            "args": [weather_script],
            "env": None
        },
        "elasticsearch-mcp-server": {
            "command": "npx",
            "args": ["-y", "@elastic/mcp-server-elasticsearch"],
            "env": {
                "ES_URL": es_url,
                "ES_API_KEY": es_api_key
            }
        },
        "aws-ses-mcp": {
            "command": "node",
            "args": [aws_ses_mcp_server_path],
            "env": {
                "AWS_ACCESS_KEY_ID": aws_access_key_id,
                "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
                "AWS_REGION": aws_region,
                "SENDER_EMAIL_ADDRESS": sender_email,
                "REPLY_TO_EMAIL_ADDRESSES": reply_to_email or sender_email
            }
        }
    }

    client = MultiServerMCPClient()
    try:
        await client.connect_to_servers(server_configs)
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())