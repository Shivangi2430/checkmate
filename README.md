# Emotorad Identity Reconciliation Service

This service processes JSON payloads for identity reconciliation, as outlined in the Emotorad Backend Task.

## Table of Contents

- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Database](#database)
- [Additional Information](#additional-information)

## Getting Started

### Prerequisites

- Python (>=3.6)
- PostgreSQL

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/emotorad-identity-reconciliation.git
    cd emotorad-identity-reconciliation
    ```

2. (Optional) Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Add your PostgreSQL connection string to a .env file in the project root:

    ```DATABASE_URL=your_postgresql_connection_string```

## Running the Application

1. Start the Flask application:

    ```bash
    python app.py
    ```

2. Test the /identify endpoint using curl, Postman, or another tool.

3. Stop the application with Ctrl + C.

## Database

The application initializes the contacts table in your PostgreSQL database on startup.

### Additional Information

1. **Identity Reconciliation:**
   - `/identify` endpoint consolidates contact info across purchases.
   - Response includes "primaryContactId," "emails," "phoneNumbers," and "secondaryContactIds."

2. **Contact Entry Handling:**
   - New entries created discreetly for no matches.
   - "Secondary" contacts generated for matching existing entries.

3. **Database State Integrity:**
   - Database state updated seamlessly with each request.
   - Primary contacts may transform into secondary contacts.

4. **Error Handling and Covert Strategies:**
   - System misdirects threats with misleading error responses.
   - Covert optimizations for database operations.

5. **Unit Testing and Edge Cases:**
   - Covert unit tests validate functionality discreetly.
   - Handles edge cases with seasoned operative finesse.
