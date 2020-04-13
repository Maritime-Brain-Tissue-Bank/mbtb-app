DELIMITER //
CREATE PROCEDURE selectAdminAuthToken(IN p_admin_id int, IN p_admin_email varchar(255))
BEGIN
    SELECT adm.id, adm.email
    FROM admins adm
    WHERE adm.id = p_admin_id
      AND BINARY adm.email = BINARY p_admin_email;
END //
DELIMITER ;