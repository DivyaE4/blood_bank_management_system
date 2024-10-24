USE donation_db;

Create the login_details table
CREATE TABLE IF NOT EXISTS login_details (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    blood_type VARCHAR(10) NOT NULL,
    contact_info VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS donation_camps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    camp_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    timings VARCHAR(100) NOT NULL,
    address TEXT NOT NULL
);

-- Create the donations table
CREATE TABLE IF NOT EXISTS donations (
    donation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    camp_name VARCHAR(255) NOT NULL,
    camp_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    timings VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES login_details(id),
    FOREIGN KEY (camp_id) REFERENCES donation_camps(id)
);


INSERT INTO donation_camps (camp_name, location, timings, address) 
VALUES 
('LifeSavers Blood Camp', 'Mumbai', '9 AM - 5 PM', 'Dr. R.N. Cooper Hospital, Vile Parle, Mumbai, Maharashtra'),
('United Blood Donors Camp', 'Mumbai', '10 AM - 6 PM', 'Tata Memorial Hospital, Parel, Mumbai, Maharashtra'),
('Red Cross Blood Donation Drive', 'Mumbai', '8 AM - 4 PM', 'Bombay Hospital, Marine Lines, Mumbai, Maharashtra'),
('Hope for Life Blood Camp', 'Mumbai', '9 AM - 5 PM', 'KEM Hospital, Parel, Mumbai, Maharashtra'),
('Healing Hands Blood Camp', 'Mumbai', '10 AM - 6 PM', 'Lilavati Hospital, Bandra West, Mumbai, Maharashtra'),

('Hope Givers Blood Drive', 'Bengaluru', '10 AM - 6 PM', 'M.S. Ramaiah Medical College, Mathikere, Bengaluru, Karnataka'),
('VitalBlood Donation Camp', 'Bengaluru', '9 AM - 5 PM', 'St. John\'s Medical College, Koramangala, Bengaluru, Karnataka'),
('RedDrop Blood Donation', 'Bengaluru', '8 AM - 4 PM', 'Manipal Hospital, Old Airport Road, Bengaluru, Karnataka'),
('LifeSource Blood Camp', 'Bengaluru', '9 AM - 5 PM', 'Bowring and Lady Curzon Hospital, Shivajinagar, Bengaluru, Karnataka'),
('Blood Bridge Donation Camp', 'Bengaluru', '10 AM - 6 PM', 'Victoria Hospital, K.R. Market, Bengaluru, Karnataka'),

('Healing Hands Blood Camp', 'Delhi', '8 AM - 4 PM', 'Safdarjung Hospital, Ansari Nagar, Delhi'),
('Red Cross Blood Donation Drive', 'Delhi', '9 AM - 5 PM', 'All India Institute of Medical Sciences (AIIMS), Ansari Nagar, Delhi'),
('Life Givers Blood Camp', 'Delhi', '10 AM - 6 PM', 'Max Super Speciality Hospital, Saket, Delhi'),
('VitalBlood Donation Camp', 'Delhi', '9 AM - 5 PM', 'Lok Nayak Hospital, Jawaharlal Nehru Marg, Delhi'),
('United Blood Donors Camp', 'Delhi', '10 AM - 6 PM', 'Fortis Hospital, Vasant Kunj, Delhi'),

('RedDrop Blood Donation', 'Hyderabad', '9 AM - 5 PM', 'NIMS Hospital, Punjagutta, Hyderabad, Telangana'),
('Hope Givers Blood Drive', 'Hyderabad', '10 AM - 6 PM', 'Osmania General Hospital, Afzalgunj, Hyderabad, Telangana'),
('LifeSource Blood Camp', 'Hyderabad', '8 AM - 4 PM', 'Apollo Hospitals, Jubilee Hills, Hyderabad, Telangana'),
('Healing Hands Blood Camp', 'Hyderabad', '9 AM - 5 PM', 'KIMS Hospitals, Secunderabad, Hyderabad, Telangana'),
('United Blood Donors Camp', 'Hyderabad', '10 AM - 6 PM', 'Care Hospitals, Banjara Hills, Hyderabad, Telangana'),

('VitalBlood Donation Drive', 'Chennai', '9 AM - 5 PM', 'Stanley Medical College, Royapuram, Chennai, Tamil Nadu'),
('Hope Givers Blood Camp', 'Chennai', '10 AM - 6 PM', 'Apollo Hospitals, Greams Road, Chennai, Tamil Nadu'),
('RedDrop Blood Donation', 'Chennai', '8 AM - 4 PM', 'Government General Hospital, Park Town, Chennai, Tamil Nadu'),
('LifeSource Blood Camp', 'Chennai', '9 AM - 5 PM', 'SRM Medical College Hospital, Kattankulathur, Chennai, Tamil Nadu'),
('United Blood Donors Camp', 'Chennai', '10 AM - 6 PM', 'Fortis Malar Hospital, Adyar, Chennai, Tamil Nadu'),

('United Blood Donors Camp', 'Kolkata', '10 AM - 6 PM', 'Calcutta National Medical College, Park Circus, Kolkata, West Bengal'),
('Hope for Life Blood Camp', 'Kolkata', '9 AM - 5 PM', 'AMRI Hospitals, Dhakuria, Kolkata, West Bengal'),
('Red Cross Blood Donation Drive', 'Kolkata', '8 AM - 4 PM', 'Apollo Gleneagles Hospitals, Salt Lake, Kolkata, West Bengal'),
('Healing Hands Blood Camp', 'Kolkata', '9 AM - 5 PM', 'Woodlands Multispeciality Hospital, Alipore, Kolkata, West Bengal'),
('LifeSource Blood Camp', 'Kolkata', '10 AM - 6 PM', 'Peerless Hospital, Panchasayar, Kolkata, West Bengal');
