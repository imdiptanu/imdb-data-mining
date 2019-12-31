/*
CSCI-620 : Group Project, Phase - I
Description: This file will create the temporary tables into the database.
Authors: 
Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
*/

-- Create temporary beer table from the dataset
CREATE TABLE IF NOT EXISTS temp_beers(
	id INTEGER PRIMARY KEY,
	name VARCHAR,
	brewery_id INTEGER,
	state VARCHAR(4),
	country VARCHAR(2),
	style VARCHAR,
	availability VARCHAR,
	abv DECIMAL DEFAULT 0.0,
	notes TEXT,
	retired BOOLEAN
);

-- Create temporary breweries table from the dataset
CREATE TABLE IF NOT EXISTS temp_breweries(
	id INTEGER PRIMARY KEY,
	name VARCHAR,
	city VARCHAR,
	state VARCHAR(4),
	country VARCHAR(2),
	notes TEXT,
	types VARCHAR[]
);

-- Create temporary reviews table from the dataset
CREATE TABLE IF NOT EXISTS temp_reviews(
	id SERIAL PRIMARY KEY,
	beer_id INTEGER,
	username VARCHAR,
	date DATE,
	text TEXT,
	look DECIMAL DEFAULT 0.0,
	smell DECIMAL DEFAULT 0.0,
	taste DECIMAL DEFAULT 0.0,
	feel DECIMAL DEFAULT 0.0,
	overall DECIMAL DEFAULT 0.0,
	score DECIMAL DEFAULT 0.0
);
