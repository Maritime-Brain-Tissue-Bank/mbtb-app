DELIMITER //
CREATE PROCEDURE selectTissueMetaData(IN p_prime_details_id int)
BEGIN
    SELECT img.file_name, n_reg.region_name, stn.stain_name
    FROM image_repository img
    LEFT JOIN n_regions n_reg
        ON img.region_id = n_reg.region_id
    LEFT JOIN stains stn
        ON img.stain_id = stn.stain_id
    WHERE BINARY img.prime_details_id = BINARY p_prime_details_id
    ORDER BY n_reg.region_name;
END //
DELIMITER ;