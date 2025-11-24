SQL - Create Tables (not in creation order):

CREATE TABLE packages (
    package_id string NOT NULL,
    name string NOT NULL,
    description text,
    items_consumed text,
	active_flag boolean,
    PRIMARY KEY (package_id)
);

CREATE TABLE stock (
    part_id string NOT NULL,
    name string NOT NULL,
    description text,
    common_repair_group text,
	active_flag boolean,
    PRIMARY KEY (part_id)
);

ALTER TABLE stock
ADD stocklevel_GRDG_001 string;

ALTER TABLE stock
ADD stocklevel_GRDG_002 string;

ALTER TABLE stock
ADD stocklevel_GRDG_003 string;

ALTER TABLE stock
ADD stocklevel_GRDG_004 string;

CREATE TABLE customer_vehicles (
    customer_vehicle_id string NOT NULL,
    customer_id string,
    car_reg string,
    car_make string,
    car_model string,
    MOT_status string,   
	active_flag boolean,	
    PRIMARY KEY (customer_vehicle_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE customer (
    customer_id string NOT NULL,
    user_id string NOT NULL,
    PRIMARY KEY (customer_id)
);

CREATE TABLE staff (
    staff_id    STRING NOT NULL,
    user_id     STRING NOT NULL,
    staff_type  STRING,
    mechanic_id STRING,
    PRIMARY KEY (
        staff_id
    )
);

CREATE TABLE postcodes (
    postcode_id string NOT NULL,
    postcode NOT NULL,
    PRIMARY KEY (postcode_id)
);

CREATE TABLE access_codes (
    access_code string NOT NULL,
    description text,
    PRIMARY KEY (access_code)
);

CREATE TABLE memberships (
    membership_id string NOT NULL,
    customer_id string NOT NULL,
    subscription_payment_day int,
    payment_method string,
    iban string,
    PRIMARY KEY (membership_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE garages (
    garage_id string NOT NULL,
    name string
    address text,
    postcode_id string,
    email string,
    phone_number int,
    contact_staff string,    
    PRIMARY KEY (garage_id),
    FOREIGN KEY (postcode_id) REFERENCES postcodes(postcode_id)
);

CREATE TABLE users (
    user_id               STRING  NOT NULL,
    name                  STRING,
    address               TEXT,
    postcode_id           STRING,
    email                 STRING,
    phone_no              INT,
    primary_garage        STRING,
    access_code           STRING  NOT NULL,
    account_creation_date DATE,
    active_flag           BOOLEAN,
    PRIMARY KEY (
        user_id
    ),
    FOREIGN KEY (
        postcode_id
    )
    REFERENCES postcodes (postcode_id),
    FOREIGN KEY (
        access_code
    )
    REFERENCES access_codes (access_code) 
);


CREATE TABLE login_details(
    user_name string NOT NULL,
    password string NOT NULL,
	user_id string NOT NULL,	
	PRIMARY KEY (user_name)
);

CREATE TABLE transactions (
    transaction_id string NOT NULL,
    booking_id string NOT NULL,
    customer_vehicle_id string NOT NULL,
    part_consumed string,
    qty_consumed int,
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (part_consumed) REFERENCES stock(part_id),
	FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (customer_vehicle_id) REFERENCES customer_vehicles(customer_vehicle_id)
);

CREATE TABLE bookings (
    bookings_id string NOT NULL,
    customer_id string NOT NULL,
    garage_id string NOT NULL,
    mechanic_id string,
    customer_vehicle_id string,
    referral text,
	referral_from text,
    package_id string,
    date_of_service date,
    followup_required boolean,
    payment_method string,
    paid boolean, 
    total_cost_net double,
    total_cost_vat double,
    total_cost_gross double,
    PRIMARY KEY (bookings_id),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (garage_id) REFERENCES garages(garage_id),
    FOREIGN KEY (customer_vehicle_id) REFERENCES customer_vehicles(customer_vehicle_id),
    FOREIGN KEY (package_id) REFERENCES packages(package_id)
);

CREATE TABLE audit_table (
    audit_record_id string NOT NULL,
    field_id string NOT NULL,
    action_type string NOT NULL,
    change_from string,
    change_to string,
    user_id string NOT NULL,
    date_of_change date,
    PRIMARY KEY (audit_record_id)
);