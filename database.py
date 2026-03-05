import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "DermaDesk"),
        port=int(os.getenv("DB_PORT", 3306))
    )

# --- PATIENT FUNCTIONS ---

def get_patient_by_phone(phone):
    """Searches for a patient by phone number."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM patients WHERE phone = %s"
        cursor.execute(query, (phone,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def create_patient(name, phone, email, age, gender):
    """Registers a new patient into the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "INSERT INTO patients (name, phone, email, age, gender) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, phone, email, age, gender))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

# --- APPOINTMENT FUNCTIONS ---

def get_booked_slots(date):
    """Returns list of times already taken (booked) for a specific date."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = "SELECT slot_time FROM appointments WHERE appt_date = %s AND status = 'booked'"
        cursor.execute(query, (date,))
        # Converts timedelta/time objects to 'HH:MM' string format
        return [str(row[0])[:5] for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

def create_booking(patient_id, date, time, reason="Dermatology Consultation"):
    """Creates a new appointment with status 'booked'."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Standardizing time to HH:MM:SS for database consistency
        formatted_time = time if len(time) == 8 else f"{time}:00"
        query = "INSERT INTO appointments (patient_id, appt_date, slot_time, reason, status) VALUES (%s, %s, %s, %s, 'booked')"
        cursor.execute(query, (patient_id, date, formatted_time, reason))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def update_booking_status(patient_id, date, time, status):
    """Updates status (e.g., 'cancelled') for a specific appointment."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Standardize time for the WHERE clause to match DB '15:00:00' format
        formatted_time = time if len(time) == 8 else f"{time}:00"
        
        query = """
            UPDATE appointments 
            SET status = %s 
            WHERE patient_id = %s AND heappt_date = %s AND slot_time = %s
            AND status = 'booked'
        """
        cursor.execute(query, (status, patient_id, date, formatted_time))
        conn.commit()
        
        # Check if any row was actually changed
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_patient_appointments(patient_id):
    """Fetches all 'booked' appointments for a specific patient."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT appt_date, slot_time, reason FROM appointments WHERE patient_id = %s AND status = 'booked'"
        cursor.execute(query, (patient_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()