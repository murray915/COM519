
--example users table
--all the same bar, the table and the columns within

	CREATE TRIGGER trg_users_after_insert
	AFTER INSERT ON users
	FOR EACH ROW
	BEGIN
		INSERT INTO audit_table(
			audit_record_id,
			action_type,
			primary_key_ref,
			change_from,
			change_to,
			date_of_change,
			time_of_change
		)
		VALUES (
			'AUD-' || printf(
				'%03d',
				COALESCE(
					(SELECT MAX(CAST(substr(audit_record_id, 5) AS INTEGER)) FROM audit_table),
					0
				) + 1
			),
			'CREATE',
			new.user_id,
			'-',
			'-',
			date('now'),
			time('now')
		);
	END;

	CREATE TRIGGER trg_users_after_delete
	AFTER DELETE ON users
	FOR EACH ROW
	BEGIN
		INSERT INTO audit_table(
			audit_record_id,
			action_type,
			primary_key_ref,
			change_from,
			change_to,
			date_of_change,
			time_of_change
		)
		VALUES (
			'AUD-' || printf(
				'%03d',
				COALESCE(
					(SELECT MAX(CAST(substr(audit_record_id, 5) AS INTEGER)) FROM audit_table),
					0
				) + 1
			),
			'DELETE',
			OLD.user_id,
			'-',
			'-',
			date('now'),
			time('now')
		);
	END;


	CREATE TRIGGER trg_users_after_update
	AFTER UPDATE ON users
	FOR EACH ROW
	BEGIN
		INSERT INTO audit_table(
			audit_record_id,
			action_type,
			primary_key_ref,
			change_from,
			change_to,
			date_of_change,
			time_of_change
		)
		VALUES (
			'AUD-' || printf(
				'%03d',
				COALESCE(
					(SELECT MAX(CAST(substr(audit_record_id, 5) AS INTEGER)) FROM audit_table),
					0
				) + 1
			),
			'UPDATE',
			NEW.user_id,
			json_object(
				'name', OLD.name,
				'address', OLD.address,
				'postcode_id', OLD.postcode_id,
				'email', OLD.email,
				'phone_no', OLD.phone_no,
				'primary_garage', OLD.primary_garage,
				'access_code', OLD.access_code,
				'account_creation_date', OLD.account_creation_date,
				'active_flag', OLD.active_flag
			),
			json_object(
				'name', NEW.name,
				'address', NEW.address,
				'postcode_id', NEW.postcode_id,
				'email', NEW.email,
				'phone_no', NEW.phone_no,
				'primary_garage', NEW.primary_garage,
				'access_code', NEW.access_code,
				'account_creation_date', NEW.account_creation_date,
				'active_flag', NEW.active_flag
			),
			date('now'),
			time('now')
		);
	END;

