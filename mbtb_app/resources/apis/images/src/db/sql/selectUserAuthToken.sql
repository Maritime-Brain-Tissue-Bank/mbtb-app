DELIMITER //
CREATE PROCEDURE selectUserAuthToken(IN p_user_id int, IN p_user_email varchar(255))
BEGIN
    SELECT usrs.id, usrs.email
    FROM users usrs
    WHERE usrs.id = p_user_id
      AND BINARY usrs.email = BINARY p_user_email;
END //
DELIMITER ;