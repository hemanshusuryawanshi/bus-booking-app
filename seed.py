from app import app
from models import db, Bus, Trip
from datetime import date, time

with app.app_context():
    # Create all tables defined in models.py
    db.create_all()
    
    # Check if we already seeded to avoid duplicates
    if not Bus.query.first():
        print("Adding sample data...")
        
        # 1. Create a Bus
        bus1 = Bus(bus_number="MH-12-AB-1234", bus_name="Volvo Multi-Axle", bus_type="AC Sleeper", total_seats=40)
        db.session.add(bus1)
        db.session.commit()
        
        # 2. Create a Trip for that Bus
        trip1 = Trip(
            bus_id=bus1.bus_id,
            source="Pune",
            destination="Mumbai",
            travel_date=date(2026, 8, 1),
            departure_time=time(10, 0),
            arrival_time=time(14, 0),
            price=750.0,
            seats_available=40
        )
        db.session.add(trip1)
        db.session.commit()
        
        print("Database seeded successfully!")
    else:
        print("Database already contains data.")