-- Create the Database
CREATE DATABASE IF NOT EXISTS DermaDesk;
USE DermaDesk;

-- 1. Create the Patients Table
CREATE TABLE IF NOT EXISTS patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL, -- This is our primary search key
    email VARCHAR(100),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the Appointments Table
CREATE TABLE IF NOT EXISTS appointments (
    appt_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    appt_date DATE NOT NULL,
    slot_time TIME NOT NULL, -- e.g., '09:00:00'
    reason VARCHAR(255),
    status ENUM('booked', 'cancelled', 'rescheduled') DEFAULT 'booked',
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------
-- 3. Insert 5 Initial Patients for Testing
-- ---------------------------------------------------------

INSERT INTO patients (name, phone, email, age, gender) VALUES 
('Arun Kumar', '9876543210', 'arun@email.com', 28, 'Male'),
('Priya Sharma', '9876543211', 'priya@email.com', 34, 'Female'),
('John Doe', '9876543212', 'john@email.com', 45, 'Male'),
('Sana Khan', '9876543213', 'sana@email.com', 22, 'Female'),
('David Miller', '9876543214', 'david@email.com', 50, 'Male');


