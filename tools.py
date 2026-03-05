# tools.py
import database
from datetime import datetime


def check_patient(phone):
    """Checks if the user is an existing patient by phone number."""
    patient = database.get_patient_by_phone(phone)
    if patient:
        return {"status": "found", "patient_id": patient["patient_id"], "name": patient["name"]}
    return {"status": "not_found"}


def register_patient(name, phone, email, age, gender):
    """Registers a new patient into the database."""
    try:
        new_id = database.create_patient(name, phone, email, age, gender)
        return {
            "status": "success",
            "patient_id": new_id,
            "message": f"Patient {name} registered successfully.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_available_slots(date_str):
    """Returns available 1-hour slots, enforcing 9-5 and 1-2 PM break."""
    master_slots = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]
    booked_slots = database.get_booked_slots(date_str)
    available = [slot for slot in master_slots if slot not in booked_slots]
    return {"date": date_str, "available_slots": available}


def manage_booking(patient_id, action, date, time, new_date=None, new_time=None):
    """Handles Book, Cancel, and Reschedule logic with date validation."""

    try:
        now = datetime.now()
        target_date = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        if target_date < now:
            return {"status": "error", "message": "Cannot manage appointments for past dates or times."}
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date or time format. Please use YYYY-MM-DD and HH:MM.",
        }

    if action == "reschedule":
        if not new_date or not new_time:
            return {"status": "error", "message": "Rescheduling requires a new date and time."}

        database.update_booking_status(patient_id, date, time, "cancelled")
        database.create_booking(patient_id, new_date, new_time, "Rescheduled Appointment")
        return {"status": "success", "message": f"Appointment moved to {new_date} at {new_time}."}

    elif action == "cancel":
        database.update_booking_status(patient_id, date, time, "cancelled")
        return {"status": "success", "message": "Appointment cancelled successfully."}

    elif action == "book":
        database.create_booking(patient_id, date, time, "General Consultation")
        return {"status": "success", "message": f"Appointment booked for {date} at {time}."}

    return {"status": "error", "message": "Invalid action requested."}


def view_appointments(patient_id):
    """Retrieves a list of upcoming appointments for the patient."""
    appointments = database.get_patient_appointments(patient_id)
    if not appointments:
        return {"status": "no_appointments", "message": "No upcoming appointments found."}
    
    # Format the dates and times for the AI to read easily
    for appt in appointments:
        appt['appt_date'] = str(appt['appt_date'])
        appt['slot_time'] = str(appt['slot_time'])
        
    return {"status": "success", "appointments": appointments}