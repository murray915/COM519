def generate_audit_triggers(table_name: str, columns: list, audit_table: str = "audit_table"):
    """
    Generates SQLite audit triggers (INSERT, UPDATE, DELETE) for a table.

    :param table_name: Name of the table to audit
    :param columns: List of column names to include in audit
    :param audit_table: Name of the audit table
    :return: dict with keys 'insert', 'update', 'delete' containing SQL strings
    """
    # Helper to create json_object from a prefix (OLD or NEW)
    def json_columns(prefix):
        return ",\n            ".join(f"'{col}', {prefix}.{col}" for col in columns)

    insert_trigger = f"""
                        CREATE TRIGGER trg_{table_name}_after_insert
                        AFTER INSERT ON {table_name}
                        FOR EACH ROW
                        BEGIN
                            INSERT INTO {audit_table}(
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
                                        (SELECT MAX(CAST(substr(audit_record_id, 5) AS INTEGER)) FROM {audit_table}),
                                        0
                                    ) + 1
                                ),
                                'CREATE',
                                NEW.{columns[0]},
                                '-',
                                json_object(
                                    {json_columns("NEW")}
                                ),
                                date('now'),
                                time('now')
                            );
                        END;
                        """

    delete_trigger = f"""
                        CREATE TRIGGER trg_{table_name}_after_delete
                        AFTER DELETE ON {table_name}
                        FOR EACH ROW
                        BEGIN
                            INSERT INTO {audit_table}(
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
                                        (SELECT MAX(CAST(substr(audit_record_id, 5) AS INTEGER)) FROM {audit_table}),
                                        0
                                    ) + 1
                                ),
                                'DELETE',
                                OLD.{columns[0]},
                                json_object(
                                    {json_columns("OLD")}
                                ),
                                '-',
                                date('now'),
                                time('now')
                            );
                        END;
                        """

    update_trigger = f"""
            CREATE TRIGGER trg_{table_name}_after_update
            AFTER UPDATE ON {table_name}
            FOR EACH ROW
            BEGIN
                INSERT INTO {audit_table}(
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
                            (SELECT MAX(CAST(substr(audit_record_id, 5) AS INTEGER)) FROM {audit_table}),
                            0
                        ) + 1
                    ),
                    'UPDATE',
                    NEW.{columns[0]},
                    json_object(
                        {json_columns("OLD")}
                    ),
                    json_object(
                        {json_columns("NEW")}
                    ),
                    date('now'),
                    time('now')
                );
            END;
            """
    return {"insert": insert_trigger, "delete": delete_trigger, "update": update_trigger}


# Example usage for the stock table
stock_columns = [
    "access_code", 
    "description"
]

triggers = generate_audit_triggers("access_codes", stock_columns)

# Print or save triggers
print(triggers["insert"])
print(triggers["delete"])
print(triggers["update"])