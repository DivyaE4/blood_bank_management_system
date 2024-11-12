DELIMITER //

CREATE PROCEDURE delete_user(IN user_id INT)
BEGIN
    -- Delete associated requests
    DELETE FROM requests WHERE recipient_id = user_id;

    -- Delete associated donations
    DELETE FROM donations WHERE user_id = user_id;

    -- Finally, delete the user
    DELETE FROM login_details WHERE id = user_id;
END;

//

DELIMITER ;