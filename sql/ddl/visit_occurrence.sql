DROP TABLE IF EXISTS $schema.visit_occurrence CASCADE;
CREATE TABLE $schema.visit_occurrence (
	visit_occurrence_id BIGINT PRIMARY KEY,
	person_id BIGINT NOT NULL,
	visit_start_date DATE,
	care_site_nm TEXT,
	visit_type_value VARCHAR(50),
	FOREIGN KEY (person_id)
        REFERENCES person (person_id)
);
