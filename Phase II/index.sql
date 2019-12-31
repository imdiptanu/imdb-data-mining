/*
CSCI-620 : Group Project, Phase - II
Description: This file will create the indexes in the database for the interesting
queries provided.
Authors: 
Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
*/

CREATE INDEX IDX_ABV_10 ON BEER USING BTREE (
	ID, NAME
) WHERE (
	ABV >= 10
);

CREATE INDEX IDX_BEER_RETIRED ON BEER USING BTREE (
	ID, NAME
) WHERE (
	RETIRED
);

CREATE INDEX IDX_OVERALL_4_8 ON REVIEWS USING BTREE (
	BEER
) WHERE (
	OVERALL >= 4.8
);

CREATE INDEX IDX_OVERALL_SCORE ON REVIEWS USING BTREE (
	BEER
) WHERE (
	OVERALL >= 4.5 AND ((LOOK + SMELL + TASTE + FEEL) / 4) >= 4.5
);

CREATE INDEX IDX_NOT_RETIRED ON BEER USING BTREE (
	ID, NAME
) WHERE (
	NOT RETIRED
);

CREATE INDEX IDX_COUNTRY_US ON BREWERY USING BTREE (
	ID, NAME, CITY, STATE
) WHERE (
	COUNTRY = 'US'
);

CREATE INDEX IDX_AVAIL_LIMITED ON AVAILABILITY USING BTREE (
	ID
) WHERE (
	LOWER(AVAILABILITY) LIKE '%limited%'
);

CREATE INDEX IDX_COUNTRY_NOT_US ON BREWERY USING BTREE (
	ID, NAME, CITY, STATE, COUNTRY
) WHERE (
	COUNTRY <> 'US'
);

CREATE INDEX IDX_TYPE_HOMEBREW ON BREWERY_TYPE USING BTREE (
	BREWERY
) WHERE (
	TYPE = 1
);

CREATE INDEX IDX_COUNTRY_STATE ON BREWERY USING BTREE (
	ID, NAME, CITY
) WHERE (
	COUNTRY = 'US' AND STATE = 'NY'
);

CREATE INDEX IDX_AVAIL_YEAR_ROUND ON AVAILABILITY USING BTREE (
	ID
) WHERE (
	AVAILABILITY = 'Year-round'
);

CREATE INDEX IDX_SCORE ON REVIEWS USING BTREE (
	BEER
) WHERE (
	((LOOK + SMELL + TASTE + FEEL) / 4) >= 4.5
);

CREATE INDEX IDX_OVERALL_4_5 ON REVIEWS USING BTREE (
	BEER
) WHERE (
	OVERALL >= 4.5
);