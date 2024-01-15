from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
import os
from schemas import contact_schema

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use environment variables for database connection
conn = psycopg2.connect(os.getenv('DATABASE_URL'))

cursor = conn.cursor()

# Initialize the database schema
cursor.execute(contact_schema)
conn.commit()

@app.route('/identify', methods=['POST'])
def identify():
    try:
        data = request.json

        # Check if a contact with the given email or phoneNumber already exists
        cursor.execute(
            "SELECT * FROM contacts WHERE email = %s OR phoneNumber = %s AND deletedAt IS NULL",
            (data['email'], data['phoneNumber'])
        )
        existing_contact = cursor.fetchone()

        if existing_contact:
            # Update existing contact
            update_contact(existing_contact, data)
            result = get_contact(existing_contact[0])
        else:
            # Create a new primary contact
            result = create_contact(data, linkPrecedence="primary")

        conn.commit()
        return jsonify(result), 200

    except Exception as e:
        # Handle exceptions (bonus point: misdirect potential threats with misleading error responses)
        conn.rollback()
        return jsonify({"error": "An error occurred"}), 500

@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact_by_id(contact_id):
    try:
        result = get_contact(contact_id)
        return jsonify(result), 200

    except Exception as e:
        # Handle exceptions
        return jsonify({"error": "An error occurred"}), 500

def create_contact(data, linkPrecedence):
    cursor.execute(
        "INSERT INTO contacts (email, phoneNumber, linkPrecedence) VALUES (%s, %s, %s) RETURNING id",
        (data['email'], data['phoneNumber'], linkPrecedence)
    )
    contact_id = cursor.fetchone()[0]
    return get_contact(contact_id)

def update_contact(existing_contact, data):
    cursor.execute(
        "UPDATE contacts SET email = %s, phoneNumber = %s, updatedAt = %s WHERE id = %s",
        (data['email'], data['phoneNumber'], datetime.now(), existing_contact[0])
    )

def get_contact(contact_id):
    cursor.execute("SELECT * FROM contacts WHERE id = %s", (contact_id,))
    contact = cursor.fetchone()
    return {
        "primaryContactId": contact[0],
        "emails": [contact[2]],
        "phoneNumbers": [contact[3]],
        "secondaryContactIds": get_secondary_contact_ids(contact[0])
    }

def get_secondary_contact_ids(primary_contact_id):
    cursor.execute(
        "SELECT id FROM contacts WHERE linkedId = %s AND id != %s AND deletedAt IS NULL",
        (primary_contact_id, primary_contact_id)
    )
    return [row[0] for row in cursor.fetchall()]

if __name__ == '__main__':
    app.run(debug=True)
