# Bus Booking Application — AWS EC2 + RDS + ALB

A full-stack bus ticket booking system deployed on traditional AWS infrastructure (EC2 + RDS), built as a capstone project for the AWS with Python certification course at Symbiosis.

## Architecture

```
Browser → ALB → EC2 (Flask app via Gunicorn + Nginx) → RDS (MySQL)
```

- **Flask** — REST API serving bus search and booking operations
- **Flask-SQLAlchemy** — ORM layer mapping Python classes to MySQL tables
- **Amazon RDS (MySQL)** — relational database storing buses, trips, and bookings
- **EC2** — hosts the Flask app, served via Gunicorn behind Nginx, managed by systemd
- **Application Load Balancer (ALB)** — routes public HTTP traffic to the EC2 instance, health-checks `/health`
- **Security groups** — layered access: ALB accepts public traffic, EC2 only accepts traffic from the ALB, RDS only accepts traffic from EC2

## Data model

**buses** — the fleet
- `bus_id`, `bus_number`, `bus_name`, `bus_type`, `total_seats`

**trips** — a specific bus running a specific route on a specific date
- `trip_id`, `bus_id` (FK), `source`, `destination`, `travel_date`, `departure_time`, `arrival_time`, `price`, `seats_available`

**bookings** — a passenger's reservation on a trip
- `booking_id`, `trip_id` (FK), `passenger_name`, `passenger_email`, `passenger_phone`, `seats_booked`, `total_amount`, `booking_status`, `created_at`

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check, used by the ALB target group |
| GET | `/buses` | List all buses |
| GET | `/trips` | Search trips — query params: `source`, `destination`, `date` |
| GET | `/trips/<trip_id>` | Get a single trip's details |
| POST | `/bookings` | Create a booking — validates seat availability, decrements `seats_available` |
| GET | `/bookings/<booking_id>` | Look up a booking confirmation |
| DELETE | `/bookings/<booking_id>` | Cancel a booking — restores seat availability |

## Running locally

```bash
python -m venv venv
source venv/Scripts/activate    # Windows Git Bash
pip install -r requirements.txt
```

Create a `.env` file with your RDS connection details:

```
DB_HOST=your-rds-endpoint
DB_USER=admin
DB_PASSWORD=your-password
DB_NAME=busbooking
```

Then:

```bash
python seed.py       # populates sample buses/trips
python app.py         # runs on http://localhost:5000
```

## Deploying

1. Create an RDS MySQL instance (`db.t3.micro`, not publicly accessible)
2. Launch an EC2 instance, install dependencies, clone this repo
3. Set environment variables (`.env`) with the RDS endpoint and credentials
4. Run the app with Gunicorn behind Nginx, managed via systemd
5. Create a target group pointing at the EC2 instance, health check path `/health`
6. Create an internet-facing ALB with a listener forwarding to the target group

## Project structure

```
.
├── app.py              # Flask API and routes
├── models.py           # SQLAlchemy table definitions
├── config.py            # Loads .env and builds the DB connection string
├── seed.py              # Populates sample data
├── requirements.txt     # Python dependencies
├── index.html           # Static frontend dashboard
└── .gitignore
```
