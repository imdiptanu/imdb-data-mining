--------------------------------------------------------------------------------------------------------------------
-- Top high abv beers we wish we could brew again. (Considering retired true with abv >= 10 and overall rating > 4.8)
--------------------------------------------------------------------------------------------------------------------
SELECT B.NAME AS RETIRED_BEER_NAME, ROUND(AVG(R.OVERALL), 2) AS BEER_RATING FROM BEER AS B 
INNER JOIN REVIEWS AS R ON B.ID = R.BEER WHERE B.RETIRED AND B.ABV >= 10.0 GROUP BY (B.ID) HAVING 
AVG(R.OVERALL) >= 4.8 ORDER BY AVG(R.OVERALL) DESC;

Without indexing: 15 seconds
With indexing: 8 seconds

--------------------------------------------------------------------------------------------------------------------
-- Top 5 beers we must try. (Considering retired false with all parameters rating greater than 4.5)
--------------------------------------------------------------------------------------------------------------------
SELECT NONR_BEERS.NAME AS BEER_NAME, ROUND(NONR_BEERS.SCORE, 2) AS BEER_SCORE, ROUND(NONR_BEERS.OVERALL, 2) AS BEER_RATING FROM
(SELECT B.NAME, AVG((R.LOOK + R.SMELL + R.TASTE + R.FEEL) / 4) AS SCORE, AVG(R.OVERALL) AS OVERALL FROM BEER AS B 
INNER JOIN REVIEWS AS R ON B.ID = R.BEER WHERE NOT B.RETIRED GROUP BY (B.ID)) AS NONR_BEERS
WHERE NONR_BEERS.SCORE >= 4.5 AND NONR_BEERS.OVERALL >= 4.5 ORDER BY NONR_BEERS.SCORE, NONR_BEERS.OVERALL DESC;

Without indexing: 32 seconds
With indexing: 24 seconds


--------------------------------------------------------------------------------------------------------------------
-- Limited beers that are available in the USA with abv > 10.0.
--------------------------------------------------------------------------------------------------------------------
SELECT B.NAME AS LIMITED_AVAIL_BEERS, BR.NAME AS BREWERY_NAME, BR.CITY || ', ' || BR.STATE AS ADDRESS FROM BEER AS B 
INNER JOIN BREWERY AS BR ON B.BREWERY = BR.ID 
INNER JOIN AVAILABILITY AS A ON B.AVAILABILITY = A.ID 
INNER JOIN REVIEWS AS R ON B.ID = R.BEER
WHERE BR.COUNTRY = 'US' AND LOWER(A.AVAILABILITY) LIKE '%limited%' AND B.ABV > 10 AND NOT B.RETIRED
GROUP BY (B.ID, BR.ID) ORDER BY AVG(R.OVERALL) DESC;

Without indexing: 321 miliseconds
With indexing: 156 miliseconds


--------------------------------------------------------------------------------------------------------------------
-- Well-liked available beers that are home-brewed outside of the USA.
--------------------------------------------------------------------------------------------------------------------
SELECT BEER_BREWERY.AVAIL_BEERS, BEER_BREWERY.BREWERY_NAME, BEER_BREWERY.ADDRESS FROM
(SELECT B.NAME AS AVAIL_BEERS, BR.NAME AS BREWERY_NAME, 
BR.CITY || ', ' || BR.STATE || ', ' || BR.COUNTRY AS ADDRESS, 
ARRAY_AGG(T.TYPE) AS TYPE FROM BEER AS B 
INNER JOIN BREWERY AS BR ON B.BREWERY = BR.ID 
INNER JOIN BREWERY_TYPE AS BT ON BR.ID = BT.BREWERY
INNER JOIN TYPE AS T ON BT.TYPE = T.ID 
WHERE BR.COUNTRY <> 'US' AND NOT B.RETIRED GROUP BY (B.ID, BR.ID)) AS BEER_BREWERY
WHERE 'Homebrew' = ANY(TYPE);

Without indexing: 500 miliseconds
With indexing: 432 miliseconds


--------------------------------------------------------------------------------------------------------------------
-- Top-rated(based on look, smell, taste and feel) beers, which are available Year-round in NY.
--------------------------------------------------------------------------------------------------------------------
SELECT B.NAME AS LIMITED_AVAIL_BEERS, BR.NAME AS BREWERY_NAME, BR.CITY AS CITY FROM BEER AS B
INNER JOIN BREWERY AS BR ON B.BREWERY = BR.ID
INNER JOIN AVAILABILITY AS A ON B.AVAILABILITY = A.ID 
INNER JOIN REVIEWS AS R ON B.ID = R.BEER
WHERE BR.COUNTRY = 'US' AND BR.STATE = 'NY' AND A.AVAILABILITY = 'Year-round' AND NOT B.RETIRED
GROUP BY (B.ID, BR.ID) ORDER BY AVG((R.LOOK + R.SMELL + R.TASTE + R.FEEL) / 4) DESC LIMIT(5);

Without indexing: 700 miliseconds
With indexing: 503 miliseconds


--------------------------------------------------------------------------------------------------------------------
-- US breweries that brew more than 1000 top rated(overall rating > 4.5) beer.
--------------------------------------------------------------------------------------------------------------------
SELECT BR.NAME, BR.CITY || ', ' || BR.STATE || ', ' || BR.COUNTRY AS ADDRESS, 
COUNT(CASE WHEN R.OVERALL > 4.5 THEN 1 END) AS OVERALL_QUALITY_BEERS
FROM BREWERY AS BR INNER JOIN BEER AS B ON BR.ID = B.BREWERY
INNER JOIN REVIEWS AS R ON B.ID = R.BEER 
WHERE BR.COUNTRY = 'US' GROUP BY (BR.ID)
HAVING COUNT(CASE WHEN R.OVERALL > 4.5 THEN 1 END) > 1000
ORDER BY OVERALL_QUALITY_BEERS DESC;

Without indexing: 20 seconds
With indexing: 16 seconds


--------------------------------------------------------------------------------------------------------------------
-- Style of beer that has the most number of beers registered.
--------------------------------------------------------------------------------------------------------------------
SELECT S.STYLE,  COUNT(B.ID) FROM STYLE AS S 
INNER JOIN BEER AS B ON S.ID = B.STYLE
GROUP BY (S.ID) ORDER BY COUNT(B.ID) DESC LIMIT(1);

Without indexing: 193 miliseconds
With indexing: 172 miliseconds