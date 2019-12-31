/*
CSCI-620 : Group Project, Phase - I
Description: This file will create the relational schema tables into the database.
Authors: 
Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
*/

-- Create the brewery table
CREATE TABLE IF NOT EXISTS Brewery(
	id INTEGER,
	name VARCHAR NOT NULL,
	city VARCHAR,
	state VARCHAR(4),
	country VARCHAR(2),
	PRIMARY KEY (id)
);

-- Create the style table
CREATE TABLE IF NOT EXISTS Style(
	id SERIAL,
	style VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY (id)
);

-- Create the type table
CREATE TABLE IF NOT EXISTS Type(
	id SERIAL,
	type TEXT NOT NULL UNIQUE,
	PRIMARY KEY (id)
);

-- Create the availability table	
CREATE TABLE IF NOT EXISTS Availability(
	id SERIAL,
	availability VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY (id)
);

-- Create the brewery_type table
CREATE TABLE IF NOT EXISTS Brewery_Type(
	brewery INTEGER,
	type INTEGER,
	PRIMARY KEY (brewery, type),
	FOREIGN KEY (brewery) REFERENCES Brewery(id),
	FOREIGN KEY (type) REFERENCES Type(id)
);

-- Create the beer table
CREATE TABLE IF NOT EXISTS Beer(
	id INTEGER,
	name VARCHAR NOT NULL,
	brewery INTEGER,
	style INTEGER,
	availability INTEGER,
	abv DECIMAL,
	retired BOOLEAN,
	PRIMARY KEY (id),
	FOREIGN KEY (brewery) REFERENCES Brewery(id),
	FOREIGN KEY (style) REFERENCES Style(id),
	FOREIGN KEY (availability) REFERENCES Availability(id)
);

-- Create the reviews table
CREATE TABLE IF NOT EXISTS Reviews(
	beer INTEGER,
	username VARCHAR,
	review_date DATE,
	review TEXT,
	look DECIMAL,
	smell DECIMAL,
	taste DECIMAL,
	feel DECIMAL,
	overall DECIMAL,
	PRIMARY KEY (beer, username, review_date),
	FOREIGN KEY (beer) REFERENCES Beer(id)
);
	

	