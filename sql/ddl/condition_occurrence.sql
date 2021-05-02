DROP TABLE IF EXISTS $schema.condition_occurrence CASCADE;
CREATE TABLE $schema.condition_occurrence (
	condition_occurrence_id BIGINT PRIMARY KEY,
	person_id BIGINT NOT NULL,
	condition_start_date DATE NOT NULL,
	condition_value TEXT,
	visit_occurrence_id BIGINT,
	FOREIGN KEY (person_id)
        REFERENCES person (person_id),
    FOREIGN KEY (visit_occurrence_id)
        REFERENCES visit_occurrence (visit_occurrence_id)
);
