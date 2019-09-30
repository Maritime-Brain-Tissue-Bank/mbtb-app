CREATE TABLE users_menu(
    id int unsigned NOT NULL AUTO_INCREMENT,
    parent int unsigned DEFAULT NULL,
    label varchar(255) DEFAULT NULL,
    link varchar(255) DEFAULT NULL,
    order_number int DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY `index2` (parent, label)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

INSERT INTO users_menu(label, link, order_number) VALUES
    ('Home', 'home/',1),
    ('Dataset', 'view_dataset/', 2),
    ('Analysis', 'analysis/', 3),
    ('FAQ', 'faq/',4);

CREATE TABLE admin_menu(
    id int unsigned NOT NULL AUTO_INCREMENT,
    parent int unsigned DEFAULT NULL,
    label varchar(255) DEFAULT NULL,
    link varchar(255) DEFAULT NULL,
    order_number int DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY `index2` (parent, label)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

INSERT INTO admin_menu(label, order_number) VALUES
    ('Home', 1),
    ('Dataset', 2),
    ('Registration Requests', 3),
    ('FAQ', 4);


INSERT INTO admin_menu(label, link, parent, order_number) VALUES
    ('View Data', 'view_dataset/', (select id from (select * from admin_menu) as `am` WHERE label='Dataset'), 1),
    ('Add New Data', 'add_new_data/', (select id from (select * from admin_menu) as `am` WHERE  label='Dataset'), 2);


INSERT INTO admin_menu(label, link, parent, order_number) VALUE
    ('View Requests', 'view_registration_requests/', (select id from (select * from admin_menu) as `am` WHERE label='Registration Requests'), 1);


UPDATE admin_menu SET link = 'home/' WHERE label = 'Home';
UPDATE admin_menu SET link = 'faq/' WHERE label = 'FAQ';
