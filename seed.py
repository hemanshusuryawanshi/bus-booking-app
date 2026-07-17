from app import app
from models import db, Bus, Trip
from datetime import date, time, timedelta
import random

# Major transit hubs in Maharashtra
cities = ["Mumbai", "Pune", "Nagpur", "Nashik", "Kolhapur", "Chhatrapati Sambhajinagar", "Solapur", "Amravati", "Thane"]

# Realistic local bus operators and types
bus_types = [
    ("MSRTC Shivneri", "AC Volvo Seater", 44),
    ("MSRTC Shivshahi", "AC Seater", 45),
    ("VRL Travels", "AC Sleeper", 30),
    ("Neeta Tours & Travels", "AC Semi-Sleeper", 40),
    ("Prasanna Purple", "Multi-Axle AC", 36),
    ("Sanjay Travels", "Non-AC Sleeper", 30)
]

with app.app_context():
    print("Clearing old database records to prevent duplicates...")
    db.drop_all()  # Wipes the old tables
    db.create_all() # Recreates them fresh

    print("Purchasing the bus fleet...")
    buses = []
    # Generate 15 random buses
    for _ in range(15):
        b_name, b_type, seats = random.choice(bus_types)
        
        # Generate a random Maharashtra license plate (e.g., MH-12-AB-9876)
        rto_code = random.randint(1, 50)
        plate_num = random.randint(1000, 9999)
        bus_number = f"MH-{rto_code:02d}-AB-{plate_num}"
        
        bus = Bus(
            bus_number=bus_number,
            bus_name=b_name,
            bus_type=b_type,
            total_seats=seats
        )
        db.session.add(bus)
        buses.append(bus)
    
    db.session.commit()
    print(f"Added {len(buses)} buses to the fleet.")

    print("Scheduling routes across Maharashtra...")
    today = date.today()
    trip_count = 0
    
    # Generate 100 random trips for the next 14 days
    for _ in range(100):
        # Pick random source and destination
        source = random.choice(cities)
        dest = random.choice(cities)
        while source == dest:
            dest = random.choice(cities) # Ensure they don't go to the same city
            
        bus = random.choice(buses)
        
        # Randomize travel dates and times
        travel_date = today + timedelta(days=random.randint(0, 14))
        departure_hour = random.randint(5, 23)
        duration = random.randint(3, 10) # 3 to 10 hour trips
        arrival_hour = (departure_hour + duration) % 24
        
        # Randomize pricing based on distance/quality
        base_price = random.uniform(400, 1800)
        price = round(base_price, -1) # Rounds to nearest 10 (e.g., 750, 1200)

        trip = Trip(
            bus_id=bus.bus_id,
            source=source,
            destination=dest,
            travel_date=travel_date,
            departure_time=time(departure_hour, 0),
            arrival_time=time(arrival_hour, 0),
            price=price,
            seats_available=bus.total_seats
        )
        db.session.add(trip)
        trip_count += 1
        
    db.session.commit()
    print(f"Successfully scheduled {trip_count} trips!")
    print("Database seeding complete.")