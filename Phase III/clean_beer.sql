/*
CSCI-620 : Group Project, Phase - III
Description: Clean beer table - where beer id is different but all other
attributes are same.
Authors: Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
*/

-- Clean beer table 

/*
Drop foreign key contraint
*/
ALTER TABLE reviews DROP CONSTRAINT reviews_beer_fkey;

/*
Any of the queries could be used to remove duplicate beer entries.
*/
DELETE FROM beer
WHERE id IN (SELECT id
FROM (SELECT id, ROW_NUMBER() OVER( PARTITION BY name, brewery, style, availability, abv, retired ORDER BY  id ) 
AS row_beer FROM beer ) b WHERE b.row_beer > 1 );

