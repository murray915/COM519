SQL - Populate/Initialise Data (In creation order):

INSERT INTO staff (staff_id, user_id)
VALUES
    ('STF-001','USR-011'),
    ('STF-002','USR-012'),
    ('STF-003','USR-013'),
    ('STF-004','USR-014'),
    ('STF-005','USR-015'),
    ('STF-006','USR-016'),
    ('STF-007','USR-017')
;

INSERT INTO postcodes (postcode_id, postcode)
VALUES 
    ('PST-001','CB2 1TN'),
    ('PST-002','SW3 4RY'),
    ('PST-003','M20 6WE'),
    ('PST-004','B15 2TH'),
    ('PST-005','LS1 4HT'),
    ('PST-006','G1 3DX'),
    ('PST-007','BS3 5RW'),
    ('PST-008','NG5 2BL'),
    ('PST-009','L1 2SR'),
    ('PST-010','S10 1AA'),
    ('PST-011','NW1 6XE'),
    ('PST-012','M14 5GH'),
    ('PST-013','B15 2TT'),
    ('PST-014','LS6 2AB'),
    ('PST-015','EH1 2NG'),
    ('PST-016','BS8 3JD'),
    ('PST-017','BN2 1RD'),
    ('PST-018','M19 1AQ'),
    ('PST-019','MK9 1BB'),
	('PST-020','LS11 5TP'),
    ('PST-021','CF10 5AE')
;

INSERT INTO garages (garage_id, name, address, postcode_id, email, phone_number, contact_staff)
VALUES 
    ('GRDG-001','Elite Motor Services','22A Kingsway Industrial Estate, Manchester','PST-018','hello@elitemotorservices.co.uk','01612 234567','Alex Soome'),
    ('GRDG-002','Greenway Auto Repairs','14 Station Road, Milton Keynes ','PST-019','contact@greenwayautorepairs.co.uk','01908 123456','Claire Yu'),
    ('GRDG-003','Parkside Vehicle Services','Unit 3, Parkside Trading Estate, Leeds','PST-020','info@parksidevehicles.co.uk','01132 345678','Ted Grass'),
    ('GRDG-004','Riverside Garage & MOT','7 Riverside Drive, Cardiff','PST-021','service@riversidegaragemot.co.uk','02920 987654','Helen Carr')
;
	
INSERT INTO stock (part_id, name, description, common_repair_group)
VALUES 
    ('ITM-001','Engine Oil','Lubricates engine components','Oil change, regular servicing',true),
    ('ITM-002','Oil Filter','Filters contaminants from engine oil','Oil change',true),
    ('ITM-003','Air Filter','Filters air entering the engine','Engine tune-up, annual service',true),
    ('ITM-004','Brake Pads','Provides friction for braking','Brake repair or replacement',true),
    ('ITM-005','Brake Discs (Rotors)','Rotating surface for brake pads to clamp','Brake system overhaul',true),
    ('ITM-006','Spark Plugs','Ignites fuel-air mixture in engine cylinders','Engine misfires, tune-up',true),
    ('ITM-007','Fuel Filter','Filters impurities from fuel','Fuel system maintenance',true),
    ('ITM-008','Timing Belt/Chain','Synchronises engine timing','Engine service (at specific mileage)',true),
    ('ITM-009','Cabin Air Filter','Filters air inside the car cabin','HVAC maintenance',true),
    ('ITM-010','Wiper Blades','Clears rain from windscreen','Seasonal maintenance',true),
    ('ITM-011','Coolant/Antifreeze','Regulates engine temperature','Cooling system flush',true),
    ('ITM-012','Transmission Fluid','Lubricates and cools transmission components','Transmission service',true),
    ('ITM-013','Battery','Powers the cars electrical system','Battery replacement',true),
    ('ITM-014','Tyres','Provides traction and supports the car’s weight','Tyre replacement or rotation',true),
    ('ITM-015','Headlight Bulbs','Provides front illumination','Bulb replacement',true)
;

INSERT INTO customer (customer_id, user_id)
VALUES
    ('CUS-001','USR-001'),
    ('CUS-002','USR-002'),
    ('CUS-003','USR-003'),
    ('CUS-004','USR-004'),
    ('CUS-005','USR-005'),
    ('CUS-006','USR-006'),
    ('CUS-007','USR-007'),
    ('CUS-008','USR-008'),
    ('CUS-009','USR-009'),
    ('CUS-010','USR-010')
;

INSERT INTO customer_vehicles (customer_vehicle_id, customer_id, car_reg, car_make, car_model, MOT_status)
VALUES
    ('CUSVEH-001','CUS-001','BK72 LXF','Volkswagen','Golf','Pass',true),
    ('CUSVEH-002','CUS-002','MV21 RYD','Volkswagen','Polo','N/A',true),
    ('CUSVEH-003','CUS-003','LD70 ZKC','Ford','Fiesta','N/A',true),
    ('CUSVEH-004','CUS-004','HY68 MJO','Nissan','Qashqai','Pass',true),
    ('CUSVEH-005','CUS-005','CN19 TXE','Ford','Fiesta','N/A',true),
    ('CUSVEH-006','CUS-006','WF73 BDU','Mercedes-Benz','C-Class','N/A',true),
    ('CUSVEH-007','CUS-007','KS22 VNM','Honda','Civic','N/A',true),
    ('CUSVEH-008','CUS-008','GX71 HLE','BMW','3 Series','Pass',true),
    ('CUSVEH-009','CUS-009','RJ69 YTB','Toyota','Corolla','N/A',true),
    ('CUSVEH-010','CUS-010','DA20 KZW','Honda','Civic','N/A',true)
;

INSERT INTO memberships (membership_id, customer_id, subscription_payment_day, payment_method, iban)
VALUES
    ('MEM-001','CUS-002','1','Card','GB00 HBUK 4012 3456 7890 12'),
    ('MEM-002','CUS-005','15','Card','GB29 NWBK 6016 1331 9268 19'),
    ('MEM-003','CUS-010','1','Card','GB82 WEST 1234 5698 7654 32')
;

INSERT INTO packages (package_id, name, description, items_consumed)
VALUES
    ('PCK-001','MOT/Service','MOT and Full Service','[ITM-001,ITM-002,ITM-003]',true),
    ('PCK-002','Cooling Sys. Referb','Cooling system check and referbish','[ITM-009,ITM-010,ITM-011]',true),
    ('PCK-003','Interim Service','Interim Service','[ITM-003,ITM-006,ITM-007]',true),
    ('PCK-004','Investigation/Service','Full review of vehicle, with feedback from customer','N/A',true)
;


INSERT INTO bookings (bookings_id, customer_id, garage_id, mechanic_id, customer_vehicle_id, referral, referral_from, package_id, date_of_service, followup_required, payment_method, paid, total_cost_net, total_cost_vat, total_cost_gross)
VALUES
    ('BK-001','CUS-001','GRDG-002','MEC-001','CUSVEH-001',true,'"Garage referal from Elite Motor Services"','PCK-001','2025-10-06',false,'Card',true,'180','36','216'),
    ('BK-002','CUS-002','GRDG-003','MEC-002','CUSVEH-002',false,'"Online"','PCK-002','2025-10-01',true,'Membership',true,'80','16','96'),
    ('BK-003','CUS-003','GRDG-003','MEC-002','CUSVEH-003',false,'"Online"','PCK-002','2025-10-15',false,'Card',true,'80','16','96'),
    ('BK-004','CUS-004','GRDG-002','MEC-001','CUSVEH-004',false,'N/A','PCK-001','2025-10-10',false,'Card',true,'180','36','216'),
    ('BK-005','CUS-005','GRDG-002','MEC-003','CUSVEH-005',false,'N/A','PCK-003','2025-10-03',false,'Membership',true,'120','24','144'),
    ('BK-006','CUS-006','GRDG-004','MEC-004','CUSVEH-006',false,'N/A','PCK-004','2025-10-18',false,'Card',true,'450','90','540'),
    ('BK-007','CUS-007','GRDG-002','MEC-001','CUSVEH-007',true,'"Garage referal from Elite Motor Services"','PCK-003','2025-10-09',false,'Cash',true,'120','24','144'),
    ('BK-008','CUS-008','GRDG-004','MEC-004','CUSVEH-008',false,'"Online"','PCK-001','2025-10-13',false,'Cash',true,'175','35','210'),
    ('BK-009','CUS-009','GRDG-002','MEC-003','CUSVEH-009',false,'"Word of Mouth"','PCK-004','2025-09-28',true,'Card',true,'85','17','102'),
    ('BK-010','CUS-010','GRDG-001','MEC-005','CUSVEH-010',false,'"Word of Mouth"','PCK-003','2025-10-16',false,'Membership',true,'140','28','168')
;

INSERT INTO transactions (transaction_id, booking_id, customer_vehicle_id, part_consumed, qty_consumed)
VALUES
    ('TACT-001','BK-001','CUSVEH-001','ITM-001','1'),
    ('TACT-002','BK-001','CUSVEH-001','ITM-002','1'),
    ('TACT-003','BK-001','CUSVEH-001','ITM-003','1'),
    ('TACT-004','BK-001','CUSVEH-001','ITM-004','4'),
    ('TACT-005','BK-002','CUSVEH-002','ITM-009','1'),
    ('TACT-006','BK-002','CUSVEH-002','ITM-010','2'),
    ('TACT-007','BK-002','CUSVEH-002','ITM-011','1'),
    ('TACT-008','BK-003','CUSVEH-003','ITM-009','1'),
    ('TACT-009','BK-003','CUSVEH-003','ITM-010','2'),
    ('TACT-010','BK-003','CUSVEH-003','ITM-011','1'),
    ('TACT-011','BK-004','CUSVEH-004','ITM-001','1'),
    ('TACT-012','BK-004','CUSVEH-004','ITM-002','1'),
    ('TACT-013','BK-004','CUSVEH-004','ITM-003','1'),
    ('TACT-014','BK-004','CUSVEH-004','ITM-004','4'),
    ('TACT-015','BK-005','CUSVEH-005','ITM-003','1'),
    ('TACT-016','BK-005','CUSVEH-005','ITM-006','6'),
    ('TACT-017','BK-005','CUSVEH-005','ITM-007','1'),
    ('TACT-018','BK-006','CUSVEH-006','ITM-001','1'),
    ('TACT-019','BK-006','CUSVEH-006','ITM-002','1'),
    ('TACT-020','BK-006','CUSVEH-006','ITM-003','1'),
    ('TACT-021','BK-006','CUSVEH-006','ITM-004','4'),
    ('TACT-022','BK-006','CUSVEH-006','ITM-005','2'),
    ('TACT-023','BK-006','CUSVEH-006','ITM-006','6'),
    ('TACT-024','BK-006','CUSVEH-006','ITM-007','1'),
    ('TACT-025','BK-006','CUSVEH-006','ITM-008','1'),
    ('TACT-026','BK-007','CUSVEH-007','ITM-003','1'),
    ('TACT-027','BK-007','CUSVEH-007','ITM-006','6'),
    ('TACT-028','BK-007','CUSVEH-007','ITM-007','1'),
    ('TACT-029','BK-008','CUSVEH-008','ITM-003','1'),
    ('TACT-030','BK-008','CUSVEH-008','ITM-004','4'),
    ('TACT-031','BK-008','CUSVEH-008','ITM-010','2'),
    ('TACT-032','BK-008','CUSVEH-008','ITM-011','1'),
    ('TACT-033','BK-009','CUSVEH-009','ITM-010','2'),
    ('TACT-034','BK-009','CUSVEH-009','ITM-011','1'),
    ('TACT-035','BK-010','CUSVEH-010','ITM-003','1'),
    ('TACT-036','BK-010','CUSVEH-010','ITM-006','6'),
    ('TACT-037','BK-010','CUSVEH-010','ITM-007','1')
;

INSERT INTO users(
	user_id,customer_id,staff_id,name,address,postcode_id,email,phone_no,membership_id,staff_type,mechanic_id,primary_garage,access_code,account_creation_date)
VALUES
    ('USR-001','CUS-001','N/A','Oliver Smith','12 High Street, Cambridge','PST-001','oliver.smith@email.com','07123 456789','N/A','N/A','N/A','N/A','CUS_USR','2025-09-12',1),
    ('USR-002','CUS-002','N/A','Amelia Jones','Flat 4, 22 King’s Road, London','PST-002','amelia.jones@email.com','07234 567890','1','N/A','N/A','N/A','CUS_USR_MEM','2025-10-25'),
    ('USR-003','CUS-003','N/A','Jack Taylor','78 Church Lane, Manchester','PST-003','jack.taylor@email.com','07345 678901','N/A','N/A','N/A','N/A','CUS_USR','2025-11-15'),
    ('USR-004','CUS-004','N/A','Olivia Brown','5 Rosewood Close, Birmingham','PST-004','olivia.brown@email.com','07456 789012','N/A','N/A','N/A','N/A','CUS_USR','2025-10-28'),
    ('USR-005','CUS-005','N/A','Harry Wilson','14 Market Street, Leeds','PST-005','harry.wilson@email.com','07567 890123','2','N/A','N/A','N/A','CUS_USR_MEM','2025-11-13'),
    ('USR-006','CUS-006','N/A','Isla Thompson','Apartment 3B, 10 Queen Street, Glasgow','PST-006','isla.thompson@email.com','07678 901234','N/A','N/A','N/A','N/A','CUS_USR','2025-08-29'),
    ('USR-007','CUS-007','N/A','Charlie Johnson','56 Victoria Road, Bristol','PST-007','charlie.johnson@email.com','07789 012345','N/A','N/A','N/A','N/A','CUS_USR','2025-11-13'),
    ('USR-008','CUS-008','N/A','Emily Walker','7 Meadow Court, Nottingham','PST-008','emily.walker@email.com','07890 123456','N/A','N/A','N/A','N/A','CUS_USR','2025-09-20'),
    ('USR-009','CUS-009','N/A','George Evans','21 Station Road, Liverpool','PST-009','george.evans@email.com','07901 234567','N/A','N/A','N/A','N/A','CUS_USR','2025-09-21'),
    ('USR-010','CUS-010','N/A','Ava Robinson','33 Green Lane, Sheffield','PST-010','ava.robinson@email.com','07012 345678','3','N/A','N/A','N/A','CUS_USR_MEM','2025-10-01'),
    ('USR-011','N/A','STF-001','Simon Lee','12 Baker Street','PST-011','Simon.Lee@email.com','07911 234567','N/A','Mechanic','MEC-01','2','STF_USR','2025-09-19'),
    ('USR-012','N/A','STF-002','Jen Keeosk','45 Oakwood Drive','PST-012','Jen.Keeosk@email.com','07941 994567','N/A','Mechanic','MEC-02','3','STF_USR','2025-11-02'),
    ('USR-013','N/A','STF-003','Jason Anderson','88 Kingsway Road','PST-013','Jason.Anderson@email.com','07722 556688','N/A','Mechanic','MEC-03','2','STF_USR','2025-10-23'),
    ('USR-014','N/A','STF-004','Jim Bean','3 Rose Hill Crescent','PST-014','Jim.Bean@email.com','07400 123456','N/A','Mechanic','MEC-04','4','STF_USR','2025-09-08'),
    ('USR-015','N/A','STF-005','Katie John','101 Castle Street','PST-015','Katie.John@email.com','020 7946 0123','N/A','Mechanic','MEC-05','1','STF_USR','2025-10-27'),
    ('USR-016','N/A','STF-006','Sue Bridges','Flat 6, 22 The Avenue','PST-016','Sue.Bridges@email.com','0121 496 0991','N/A','Front Desk','FRNT-01','1','ADMIN','2025-09-11'),
    ('USR-017','N/A','STF-007','Alex Towns','9 Seaview Terrace','PST-017','Alex.Towns@email.com','0131 225 5630','N/A','Front Desk','FRNT-02','2','ADMIN','2025-09-20')
;

INSERT INTO login_details (  
    user_name,
    password,
    user_id)
VALUES
    ('USR-01','osmith1','62683712'),
    ('USR-02','ajones1','62724718'),
    ('USR-03','jtaylor1','68582101'),
    ('USR-04','obrown1','56473833'),
    ('USR-05','hwilson1','51541186'),
    ('USR-06','ithompson1','75619299'),
    ('USR-07','cjohnson1','17127492'),
    ('USR-08','ewalker1','56375618'),
    ('USR-09','gevans1','65262483'),
    ('USR-10','arobinson1','35489144'),
    ('USR-11','slee1','40998464'),
    ('USR-12','jkeeosk1','15237089'),
    ('USR-13','janderson1','60874572'),
    ('USR-14','jbean1','94236619'),
    ('USR-15','kjohn1','17607649'),
    ('USR-16','sbridges1','95168737'),
    ('USR-17','atowns1','54083180')
;

