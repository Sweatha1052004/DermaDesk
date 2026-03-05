# tool_schema.py

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_patient",
            "description": "Checks if a patient exists in the clinic database using their phone number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone": {"type": "string", "description": "The 10-digit phone number."}
                },
                "required": ["phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "register_patient",
            "description": "Registers a new patient. Use only if check_patient returns 'not_found'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"},
                    "age": {"type": "integer"},
                    "gender": {"type": "string", "enum": ["Male", "Female", "Other"]}
                },
                "required": ["name", "phone", "age", "gender"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_available_slots",
            "description": "Retrieves 1-hour slots for a date. Clinic: 9-5 (Break 1-2 PM).",
            "parameters": {
                "type": "object",
                "properties": {
                    "date_str": {"type": "string", "description": "YYYY-MM-DD"}
                },
                "required": ["date_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "manage_booking",
            "description": "Book, cancel, or reschedule appointments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "integer"},
                    "action": {"type": "string", "enum": ["book", "cancel", "reschedule"]},
                    "date": {"type": "string", "description": "Current/Old appt date (YYYY-MM-DD)"},
                    "time": {"type": "string", "description": "Current/Old appt time (HH:MM)"},
                    "new_date": {"type": "string", "description": "New date for rescheduling"},
                    "new_time": {"type": "string", "description": "New time for rescheduling"},
                    "reason": {"type": "string", "description": "User's reason for the visit/reschedule"}
                },
                "required": ["patient_id", "action", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "view_appointments",
            "description": "Look up all upcoming scheduled appointments for a specific patient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "integer"}
                },
                "required": ["patient_id"]
            }
        }
    }
]