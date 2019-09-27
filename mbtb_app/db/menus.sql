create table users_menu(
    id int unsigned not null auto_increment,
    parent int unsigned default null,
    label varchar(255) DEFAULT NULL,
    link varchar(255) DEFAULT NULL,
    order_number int default null,
    primary key (id),
    unique key `index2` (parent, label)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into users_menu(label, link, order_number) values
    ('Home', 'home/',1),
    ('Dataset', 'view_dataset/', 2),
    ('Analysis', 'analysis/', 3),
    ('FAQ', 'faq/',4);

create table admin_menu(
    id int unsigned not null auto_increment,
    parent int unsigned default null,
    label varchar(255) DEFAULT NULL,
    link varchar(255) DEFAULT NULL,
    order_number int default null,
    primary key (id),
    unique key `index2` (parent, label)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into admin_menu(label, order_number) values
    ('Home', 1),
    ('Dataset', 2),
    ('Registration Requests', 3),
    ('FAQ', 4);

insert into admin_menu(label, link, parent, order_number) values
    ('View Data', 'view_dataset/', (select id from admin_menu where label='Dataset'), 1),
    ('Add New Data', 'add_new_data/', (select id from admin_menu where  label='Dataset'), 2);

insert into admin_menu(label, link, parent, order_number) value
    ('View Requests', 'view_registration_requests/', (select id from admin_menu where label='Registration Requests'), 1);
