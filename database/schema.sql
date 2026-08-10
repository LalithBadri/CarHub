-- CarHub database schema
-- Run this once against your MySQL server to create the database, tables,
-- and a small set of sample cars for the rental fleet.

CREATE DATABASE IF NOT EXISTS carhub;
USE carhub;

-- Fleet of cars available for rent
CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    car_type VARCHAR(20) NOT NULL,      -- Hatchback / Sedan / SUV
    transmission VARCHAR(20) NOT NULL,  -- Manual / Automatic
    seats INT NOT NULL,
    rate_per_day DECIMAL(10, 2) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE
);

-- Every rental booking made through the site
CREATE TABLE IF NOT EXISTS rental_bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(id)
);

-- Every "sell my car" price-estimate request made through the site
CREATE TABLE IF NOT EXISTS car_sale_estimates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    purchase_year INT NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    mileage_km INT NOT NULL,
    condition_grade VARCHAR(20) NOT NULL, -- Excellent / Good / Fair / Poor
    estimated_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample rental fleet
INSERT INTO cars (brand, model, car_type, transmission, seats, rate_per_day, available) VALUES
('Maruti Suzuki', 'Swift', 'Hatchback', 'Manual', 5, 1200.00, TRUE),
('Hyundai', 'i20', 'Hatchback', 'Automatic', 5, 1400.00, TRUE),
('Honda', 'City', 'Sedan', 'Automatic', 5, 2000.00, TRUE),
('Maruti Suzuki', 'Dzire', 'Sedan', 'Manual', 5, 1600.00, TRUE),
('Hyundai', 'Creta', 'SUV', 'Automatic', 5, 2800.00, TRUE),
('Mahindra', 'XUV700', 'SUV', 'Automatic', 7, 3200.00, TRUE),
('Toyota', 'Innova Crysta', 'SUV', 'Manual', 7, 3500.00, TRUE),
('Tata', 'Nexon', 'SUV', 'Manual', 5, 1900.00, TRUE);
