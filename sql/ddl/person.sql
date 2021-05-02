DROP TABLE IF EXISTS $schema.person CASCADE;
CREATE TABLE $schema.person (
	person_id BIGINT PRIMARY KEY,
	year_of_birth INT NOT NULL,
	month_of_birth INT,
	day_of_birth INT,
	death_date TIMESTAMP,
	gender_value VARCHAR(50),
	race_value VARCHAR(50),
	ethnicity_value VARCHAR(50)
);
