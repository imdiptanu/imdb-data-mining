/*
CSCI-620 : Group Project, Phase - III
Description: This file is to clean reviews table where review is null and all
other parameters are 0.
Authors: Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
*/

-- Clean reviews table 

/*
Delete unmeaningfull reviews where review is blank and all other parameters are 0.
*/

DELETE FROM REVIEWS WHERE (beer, username, review_date) IN
(SELECT beer, username, review_date FROM reviews WHERE review = '' AND 
	look = 0 AND smell = 0 AND taste = 0 AND feel = 0 AND overall = 0);

/*
Create index on reviews and beer table for faster execution
*/
CREATE INDEX beer_id_idx ON beer(id);
CREATE INDEX reviews_beer_idx ON reviews(beer);

/*
Delete reviews for those beers, which does not exist anymore.
*/

CREATE TEMP TABLE temp AS SELECT r.* FROM reviews AS r LEFT JOIN
beer AS b ON b.id = r.beer WHERE b.id IS NOT NULL;

TRUNCATE reviews;

INSERT INTO reviews SELECT * FROM temp;

DROP TABLE temp;

/**
Put the Foreign key contraint back
*/
ALTER TABLE reviews 
ADD CONSTRAINT reviews_beer_fkey FOREIGN KEY (beer) REFERENCES beer(id);


