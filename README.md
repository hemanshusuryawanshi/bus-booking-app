\# Cloud-Native Bus Booking Portal 🚌



A full-stack, cloud-native bus reservation system deployed on AWS. This capstone project demonstrates a production-ready web architecture using a decoupled frontend/backend and a relational cloud database.



\## 🏗️ System Architecture

\*\*Browser → GitHub Pages → AWS ALB → EC2 (Gunicorn + Nginx) → Flask API → AWS RDS (MySQL)\*\*



\* \*\*Frontend:\*\* HTML5 / CSS3 / JavaScript (Hosted on GitHub Pages)

\* \*\*Backend:\*\* Python 3 / Flask / SQLAlchemy

\* \*\*Database:\*\* AWS RDS (MySQL)

\* \*\*Compute:\*\* AWS EC2 (Ubuntu) running Gunicorn \& Nginx

\* \*\*Networking:\*\* AWS Application Load Balancer (ALB) across multiple Availability Zones



\## ✨ Core Features

\* \*\*Live Inventory Search:\*\* Queries the RDS MySQL database for available routes in real-time.

\* \*\*Interactive Seat Mapping:\*\* Dynamically generates a 40-seat grid, locking unavailable seats based on live DB metrics.

\* \*\*Stateful Booking:\*\* Deducts available seats atomically upon booking confirmation.

\* \*\*Passenger Authentication:\*\* Captures local user session details to attach real passenger data to API payloads.



\## 🚀 Deployment

The backend REST API is hosted on an AWS EC2 instance as a background `systemd` service, placed behind an internet-facing Application Load Balancer. The frontend is a static Single Page Application (SPA) deployed via GitHub Pages, calling the AWS ALB endpoint directly.

