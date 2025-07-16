# QuickDocs Portal - Docker Deployment

This image runs the QuickDocs Portal, a business-oriented document sharing platform with a demonstrable IDOR vulnerability for educational purposes.

## Usage

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd flask-idor-lab
   ```
2. Start the services:
   ```sh
   docker-compose up
   ```

- The web application will be available at [http://localhost:5000](http://localhost:5000)
- The MySQL database will be available on port 3306 (internal use)

## Environment Variables
- `DB_HOST` (default: db)
- `DB_USER` (default: cyberlab_user)
- `DB_PASSWORD` (default: cyberlab_pwd)
- `DB_NAME` (default: cyberlab)
- `FLASK_ENV` (default: production)

## Database Initialization
The database is automatically initialized and seeded with demo users and a confidential document (ID 42) for testing the IDOR scenario.

## Access
- Home: `/`
- User dashboard: `/lab`
- Login: `/login`
- Register: `/register`

## License
For educational use only. 