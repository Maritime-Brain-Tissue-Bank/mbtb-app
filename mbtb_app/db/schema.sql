CREATE TABLE users(
    id int unsigned NOT NULL AUTO_INCREMENT,
    email varchar(255) NOT NULL DEFAULT '',
    password_hash varchar(255) DEFAULT NULL,
    title varchar(10) DEFAULT NULL,
    first_name varchar(255) DEFAULT NULL,
    middle_name varchar(255) DEFAULT NULL,
    last_name varchar(255) DEFAULT NULL,
    institution varchar(255) DEFAULT NULL,
    department_name varchar(255) DEFAULT NULL,
    position_title varchar(255) DEFAULT NULL,
    address_line_1 varchar(255) DEFAULT NULL,
    address_line_2 varchar(255) DEFAULT NULL,
    city varchar(255) DEFAULT NULL,
    province varchar(255) DEFAULT NULL,
    country varchar(255) DEFAULT NULL,
    postal_code varchar(255) DEFAULT NULL,
    comments text DEFAULT NULL,
    active_since date DEFAULT NULL,
    pending_approval enum('Y','N') DEFAULT 'Y',
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE admins(
    id int unsigned NOT NULL AUTO_INCREMENT,
    email varchar(255) NOT NULL DEFAULT '',
    password_hash varchar(255) DEFAULT NULL,
    first_name varchar(255) DEFAULT NULL,
    last_name varchar(255) DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


INSERT INTO admins(email, password_hash, first_name) VALUE
    ('admin@mbtb.ca', 'asdfghjkl123', 'admin')


CREATE TABLE neuropathological_diagnosis(
    neuro_diagnosis_id int unsigned NOT NULL AUTO_INCREMENT,
    neuro_diagnosis_name varchar(255) NOT NULL,
    PRIMARY KEY (neuro_diagnosis_id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


INSERT INTO neuropathological_diagnosis(neuro_diagnosis_name) VALUES
    ('ALCOHOLIC CEREBELLAR DEGENERATION'),
    ('AMYOTROPHIC LATERAL SCLEROSIS'),
    ('ALZHEIMER''S DISEASE'),
    ('BRAIN TUMOUR'),
    ('CEREBELLAR CORTICAL DEGENERATION'),
    ('CHRONIC MENIGOENCEPHALITIS'),
    ('CORTICOBASALGANGLIONIC DEGENERATOIN'),
    ('DOWN''S SYNDROME'),
    ('FAHR''S DISEASE'),
    ('FAMILIAL ALZHEIMER''S DISEASE'),
    ('FRONTOTEMPORAL DEMENTIA'); -- To Do: Need to add all diseases


CREATE TABLE autopsy_types(
    autopsy_type_id int unsigned NOT NULL AUTO_INCREMENT,
    autopsy_type varchar(255) NOT NULL,
    PRIMARY KEY (autopsy_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


INSERT INTO autopsy_types(autopsy_type) VALUES
    ('Brain'),
    ('Brain & Spinal'),
    ('Full Body');


CREATE TABLE tissue_types(
    tissue_type_id int unsigned NOT NULL AUTO_INCREMENT,
    tissue_type varchar(255) NOT NULL,
    PRIMARY KEY (tissue_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


INSERT INTO tissue_types(tissue_type) VALUES
    ('Brain'),
    ('Spinal Cord'),
    ('Ocular');


CREATE TABLE prime_details(
    prime_details_id int unsigned NOT NULL AUTO_INCREMENT,
    mbtb_code varchar(255) NOT NULL UNIQUE,
    sex enum('Male', 'Female') DEFAULT NULL,
    age varchar(50) DEFAULT NULL,
    postmortem_interval varchar(255) DEFAULT NULL,
    time_in_fix varchar(255) DEFAULT NULL,
    clinical_diagnosis varchar(255) DEFAULT NULL,
    neuro_diagnosis_id int unsigned NOT NULL,
    tissue_type_id int unsigned NOT NULL,
    preservation_method enum('Formalin-Fixed', 'Fresh Frozen', 'Both') DEFAULT NULL, -- To Do: Yet to be confirmed
    storage_year datetime NOT NULL,
    archive enum('Yes', 'No') DEFAULT 'No',
    PRIMARY KEY (prime_details_id),
    FOREIGN KEY (neuro_diagnosis_id)
        REFERENCES neuropathological_diagnosis(neuro_diagnosis_id)
        ON DELETE no action,
    FOREIGN KEY (tissue_type_id)
        REFERENCES tissue_types(tissue_type_id)
        ON DELETE no action
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE image_repository(
    image_id int unsigned NOT NULL AUTO_INCREMENT,
    prime_details_id int unsigned NOT NULL,
    file_name varchar(255) NOT NULL,
    description text DEFAULT NULL,
    file_type varchar(255) NOT NULL,
    file_size int(20) NOT NULL,
    category enum('gross', 'raw', 'cleaned'), -- To Do: Yet to be defined
    notes text DEFAULT NULL,
    date_taken date DEFAULT NULL,
    date_inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (image_id),
    FOREIGN KEY (prime_details_id)
        REFERENCES prime_details(prime_details_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE other_details(
    other_details_id int unsigned NOT NULL AUTO_INCREMENT,
    prime_details_id int unsigned NOT NULL,
    race varchar(255) DEFAULT NULL,
    duration int(3) DEFAULT NULL,
    clinical_details text DEFAULT NULL,
    cause_of_death varchar(255) DEFAULT NULL,
    brain_weight int(5) DEFAULT NULL,
    neuropathology_summary text DEFAULT NULL,
    neuropathology_gross text DEFAULT NULL,
    neuropathology_microscopic text DEFAULT NULL,
    neouropathology_criteria varchar(255) DEFAULT NULL, -- To Do: redundant column as per update on Nov 26, 2019
    cerad varchar(255) DEFAULT NULL,
    braak_stage varchar(255) DEFAULT NULL,
    khachaturian varchar(255) DEFAULT NULL,
    abc varchar(255) DEFAULT NULL,
    autopsy_type_id int unsigned NOT NULL,
    formalin_fixed enum('True', 'False') DEFAULT NULL,
    fresh_frozen enum('True', 'False') DEFAULT NULL,
    PRIMARY KEY (other_details_id),
    FOREIGN KEY (prime_details_id)
        REFERENCES prime_details(prime_details_id)
        ON DELETE CASCADE,
    FOREIGN KEY (autopsy_type_id)
        REFERENCES autopsy_types(autopsy_type_id)
        ON DELETE no action
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE tissue_requests(
    tissue_requests_id int unsigned NOT NULL AUTO_INCREMENT,
    title varchar(10) DEFAULT NULL,
    first_name varchar(255) DEFAULT NULL,
    last_name varchar(255) DEFAULT NULL,
    email varchar(255) NOT NULL DEFAULT '',
    institution varchar(255) DEFAULT NULL,
    department_name varchar(255) DEFAULT NULL,
    city varchar(255) DEFAULT NULL,
    province varchar(255) DEFAULT NULL,
    postal_code varchar(255) DEFAULT NULL,
    phone_number varchar(255) DEFAULT NULL,
    fax_number varchar(255) DEFAULT NULL,
    project_title text DEFAULT NULL,
    source_of_funding text DEFAULT NULL,
    abstract text DEFAULT NULL,
    pending_approval enum('Y','N') DEFAULT 'Y',
    received_date date DEFAULT NULL,
    approval_date date DEFAULT NULL,
    reverted_date date DEFAULT NULL,
    tissue_request_number varchar(255) DEFAULT NULL,
    PRIMARY KEY (tissue_requests_id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
