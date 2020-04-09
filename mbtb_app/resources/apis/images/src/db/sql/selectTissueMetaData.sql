DELIMITER //
CREATE PROCEDURE selectTissueMetaData(IN p_prime_details_id int)
BEGIN
    SELECT * FROM image_repository WHERE BINARY image_repository.prime_details_id = BINARY p_prime_details_id;
END //
DELIMITER ;