-- if qty less than 5 it is automatically set to approved
DELIMITER //

CREATE TRIGGER before_insert_request
BEFORE INSERT ON requests
FOR EACH ROW
BEGIN
    IF NEW.quantity < 5 THEN
        SET NEW.status = 'approved';
    ELSE
        SET NEW.status = 'pending';
    END IF;
END //

DELIMITER ;

-- increases count of donations
ALTER TABLE donation_camps ADD COLUMN donation_count INT DEFAULT 0;

DELIMITER //

CREATE TRIGGER after_insert_donation
AFTER INSERT ON donations
FOR EACH ROW
BEGIN
    UPDATE donation_camps
    SET donation_count = donation_count + 1
    WHERE id = NEW.camp_id;
END //

DELIMITER ;

-- changes when more than 5
CREATE TABLE request_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT,
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    change_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES requests(request_id)
);

DELIMITER //

CREATE TRIGGER before_update_request
BEFORE UPDATE ON requests
FOR EACH ROW
BEGIN
    INSERT INTO request_logs (request_id, old_status, new_status)
    VALUES (OLD.request_id, OLD.status, NEW.status);
END //

DELIMITER ;

DELIMITER //

-- contact info is unique 
CREATE TRIGGER before_insert_login_details
BEFORE INSERT ON login_details
FOR EACH ROW
BEGIN
    DECLARE existing_count INT;
    SELECT COUNT(*) INTO existing_count FROM login_details WHERE contact_info = NEW.contact_info;
    IF existing_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Contact info must be unique.';
    END IF;
END //

DELIMITER ;

DELIMITER //

-- adds timestamp to requests
CREATE TRIGGER before_insert_request_timestamp
BEFORE INSERT ON requests
FOR EACH ROW
BEGIN
    SET NEW.request_date = NOW();
END //

DELIMITER ;

