from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db, Bus, Trip, Booking

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/trips', methods=['GET'])
def search_trips():
    source = request.args.get('source')
    destination = request.args.get('destination')
    
    query = Trip.query
    if source and destination:
        query = query.filter(Trip.source == source, Trip.destination == destination)
        
    trips = query.all()
    return jsonify([{
        'trip_id': t.trip_id,
        'bus_name': t.bus.bus_name,
        'source': t.source,
        'destination': t.destination,
        'departure_time': str(t.departure_time),
        'price': t.price,
        'seats_available': t.seats_available
    } for t in trips]), 200

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.json
    trip = Trip.query.get(data['trip_id'])
    
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
        
    seats_requested = int(data['seats_booked'])
    
    if trip.seats_available < seats_requested:
        return jsonify({'error': 'Not enough seats available'}), 400
        
    # Deduct seats and create booking
    trip.seats_available -= seats_requested
    
    new_booking = Booking(
        trip_id=trip.trip_id,
        passenger_name=data['passenger_name'],
        passenger_email=data['passenger_email'],
        passenger_phone=data['passenger_phone'],
        seats_booked=seats_requested,
        total_amount=trip.price * seats_requested
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Booking successful',
        'booking_id': new_booking.booking_id
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)