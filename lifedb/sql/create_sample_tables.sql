CREATE TABLE sample.regions (
	region_id INTEGER PRIMARY KEY,
	region_name CHARACTER VARYING (25)
);

CREATE TABLE sample.countries (
	country_id CHARACTER (2) PRIMARY KEY,
	country_name CHARACTER VARYING (40),
	region_id INTEGER NOT NULL,
	FOREIGN KEY (region_id) REFERENCES sample.regions (region_id)
);

CREATE TABLE sample.locations (
	location_id INTEGER PRIMARY KEY,
	street_address CHARACTER VARYING (40),
	postal_code CHARACTER VARYING (12),
	city CHARACTER VARYING (30) NOT NULL,
	state_province CHARACTER VARYING (25),
	country_id CHARACTER (2) NOT NULL,
	FOREIGN KEY (country_id) REFERENCES sample.countries (country_id)
);

CREATE TABLE sample.departments (
	department_id INTEGER PRIMARY KEY,
	department_name CHARACTER VARYING (30) NOT NULL,
	location_id INTEGER,
	FOREIGN KEY (location_id) REFERENCES sample.locations (location_id)
);

CREATE TABLE sample.jobs (
	job_id INTEGER PRIMARY KEY,
	job_title CHARACTER VARYING (35) NOT NULL,
	min_salary NUMERIC (8, 2),
	max_salary NUMERIC (8, 2)
);

CREATE TABLE sample.employees (
	employee_id INTEGER PRIMARY KEY,
	first_name CHARACTER VARYING (20),
	last_name CHARACTER VARYING (25) NOT NULL,
	email CHARACTER VARYING (100) NOT NULL,
	phone_number CHARACTER VARYING (20),
	hire_date DATE NOT NULL,
	job_id INTEGER NOT NULL,
	salary NUMERIC (8, 2) NOT NULL,
	manager_id INTEGER,
	department_id INTEGER,
	FOREIGN KEY (job_id) REFERENCES sample.jobs (job_id),
	FOREIGN KEY (department_id) REFERENCES sample.departments (department_id),
	FOREIGN KEY (manager_id) REFERENCES sample.employees (employee_id)
);

CREATE TABLE sample.dependents (
	dependent_id INTEGER PRIMARY KEY,
	first_name CHARACTER VARYING (50) NOT NULL,
	last_name CHARACTER VARYING (50) NOT NULL,
	relationship CHARACTER VARYING (25) NOT NULL,
	employee_id INTEGER NOT NULL,
	FOREIGN KEY (employee_id) REFERENCES sample.employees (employee_id)
);
