DROP TABLE IF EXISTS $schema.drug_exposure CASCADE;
CREATE TABLE $schema.drug_exposure (
	drug_exposure_id BIGINT PRIMARY KEY,
	person_id BIGINT NOT NULL,
	drug_exposure_start_date DATE NOT NULL,
	drug_value TEXT,
	route_value VARCHAR(50),
	dose_value VARCHAR(50),
	unit_value VARCHAR(50),
	visit_occurrence_id BIGINT,
	FOREIGN KEY (person_id)
        REFERENCES person (person_id),
    FOREIGN KEY (visit_occurrence_id)
        REFERENCES visit_occurrence (visit_occurrence_id)
);
