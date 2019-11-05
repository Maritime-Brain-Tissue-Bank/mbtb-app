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
    comments varchar(255) DEFAULT NULL,
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


CREATE TABLE neurodegenerative_diseases(
    neuro_diseases_id int unsigned NOT NULL AUTO_INCREMENT,
    disease_name varchar(255) NOT NULL,
    PRIMARY KEY (neuro_diseases_id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


INSERT INTO neurodegenerative_diseases(disease_name) VALUES
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


CREATE TABLE autopsy_type(
    autopsy_type_id int unsigned NOT NULL AUTO_INCREMENT,
    autopsy_type varchar(255) NOT NULL,
    PRIMARY KEY (autopsy_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


INSERT INTO autopsy_type(autopsy_type) VALUES
    ('Brain'),
    ('Brain & Spinal'),
    ('Full Body');


CREATE TABLE tissue_type(
    tissue_type_id int unsigned NOT NULL AUTO_INCREMENT,
    tissue_type varchar(255) NOT NULL,
    PRIMARY KEY (tissue_type_id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


INSERT INTO tissue_type(tissue_type) VALUES
    ('Brain'),
    ('Spinal Cord'),
    ('Ocular');


CREATE TABLE brain_dataset(
    brain_data_id int unsigned NOT NULL AUTO_INCREMENT,
    mbtb_code varchar(255) NOT NULL,
    sex enum('Male', 'Female') DEFAULT NULL,
    age varchar(50) DEFAULT NULL,
    postmortem_interval varchar(255) DEFAULT NULL,
    time_in_fix varchar(255) DEFAULT NULL,
    neuro_diseases_id int unsigned NOT NULL,
    tissue_type_id int unsigned NOT NULL,
    storage_method enum('Fresh', 'Not Fresh') DEFAULT NULL, -- To Do: Yet to be defined
    storage_year datetime NOT NULL,
    archive enum('Yes', 'No') DEFAULT 'No',
    PRIMARY KEY (brain_data_id),
    FOREIGN KEY (neuro_diseases_id)
        REFERENCES neurodegenerative_diseases(neuro_diseases_id)
        ON DELETE no action,
    FOREIGN KEY (tissue_type_id)
        REFERENCES tissue_type(tissue_type_id)
        ON DELETE no action
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE image_repository(
    image_id int unsigned NOT NULL AUTO_INCREMENT,
    brain_data_id int unsigned NOT NULL,
    file_name varchar(255) NOT NULL,
    description text DEFAULT NULL,
    file_type varchar(255) NOT NULL,
    file_size int(20) NOT NULL,
    category enum('gross', 'raw', 'cleaned'), -- To Do: Yet to be defined
    notes text DEFAULT NULL,
    date_taken date DEFAULT NULL,
    date_inserted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (image_id),
    FOREIGN KEY (brain_data_id)
        REFERENCES brain_dataset(brain_data_id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE dataset_othr_details(
    othr_details_id int unsigned NOT NULL AUTO_INCREMENT,
    brain_data_id int unsigned NOT NULL,
    race varchar(255) DEFAULT NULL,
    diagnosis_of_dementia varchar(255) DEFAULT NULL,
    duration_of_dementia int(3) DEFAULT NULL,
    clinical_history text DEFAULT NULL,
    cause_of_death varchar(255) DEFAULT NULL,
    brain_weight int(5) DEFAULT NULL,
    neuoropathology_detailed text DEFAULT NULL,
    neuropathology_gross text DEFAULT NULL,
    neuropathology_micro text DEFAULT NULL,
    neouropathology_criteria varchar(255) DEFAULT NULL,
    cerad varchar(255) DEFAULT NULL,
    braak_stage varchar(255) DEFAULT NULL,
    khachaturian varchar(255) DEFAULT NULL,
    abc varchar(255) DEFAULT NULL,
    autopsy_type_id int unsigned NOT NULL,
    tissue_type_formalin_fixed enum('True', 'False') DEFAULT NULL,
    PRIMARY KEY (othr_details_id),
    FOREIGN KEY (brain_data_id)
        REFERENCES brain_dataset(brain_data_id)
        ON DELETE CASCADE,
    FOREIGN KEY (autopsy_type_id)
        REFERENCES autopsy_type(autopsy_type_id)
        ON DELETE no action
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
