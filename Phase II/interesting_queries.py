"""
CSCI-620: Group Project, Phase - II
Description: This file will run the interesting queries provided and print
the timing to run the queries.
Authors:
Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
"""

# Importing python3 libraries for the project
import time
import psycopg2


def query1(connection):
    """
    This method is to fetch top high abv beers we wish could be brewed again.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("""SELECT B.NAME AS RETIRED_BEER_NAME, ROUND(AVG(R.OVERALL), 2) 
    AS BEER_RATING FROM BEER AS B INNER JOIN REVIEWS AS R ON B.ID = R.BEER 
    WHERE B.RETIRED AND B.ABV >= 10.0 GROUP BY (B.ID) HAVING 
    AVG(R.OVERALL) >= 4.8 ORDER BY AVG(R.OVERALL) DESC;""")
    print("%.3f" % (time.time() - current), "seconds to execute the query 1.")


def query2(connection):
    """
    This method is to fetch top 5 beers we must try based on score and rating.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("""SELECT NONR_BEERS.NAME AS BEER_NAME, ROUND(NONR_BEERS.SCORE, 2) AS BEER_SCORE, 
    ROUND(NONR_BEERS.OVERALL, 2) AS BEER_RATING FROM (SELECT B.NAME, AVG((R.LOOK + R.SMELL + R.TASTE + R.FEEL) / 4)
    AS SCORE, AVG(R.OVERALL) AS OVERALL FROM BEER AS B 
    INNER JOIN REVIEWS AS R ON B.ID = R.BEER WHERE NOT B.RETIRED GROUP BY (B.ID)) AS NONR_BEERS
    WHERE NONR_BEERS.SCORE >= 4.5 AND NONR_BEERS.OVERALL >= 4.5 
    ORDER BY NONR_BEERS.SCORE, NONR_BEERS.OVERALL DESC;""")
    print("%.3f" % (time.time() - current), "seconds to execute the query 2.")


def query3(connection):
    """
    This method is to fetch limited beers that are available in the USA with high abv
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("""SELECT B.NAME AS LIMITED_AVAIL_BEERS, BR.NAME AS BREWERY_NAME, 
    BR.CITY || ', ' || BR.STATE AS ADDRESS FROM BEER AS B INNER JOIN BREWERY 
    AS BR ON B.BREWERY = BR.ID  INNER JOIN AVAILABILITY AS A ON B.AVAILABILITY = A.ID 
    INNER JOIN REVIEWS AS R ON B.ID = R.BEER
    WHERE BR.COUNTRY = 'US' AND LOWER(A.AVAILABILITY) LIKE '%limited%' AND B.ABV > 10 AND NOT B.RETIRED
    GROUP BY (B.ID, BR.ID) ORDER BY AVG(R.OVERALL) DESC;""")
    print("%.3f" % (time.time() - current), "seconds to execute the query 3.")


def query4(connection):
    """
    This method is to fetch well-liked available beers that are home-brewed outside of the USA
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("""SELECT BEER_BREWERY.AVAIL_BEERS, BEER_BREWERY.BREWERY_NAME, BEER_BREWERY.ADDRESS FROM
    (SELECT B.NAME AS AVAIL_BEERS, BR.NAME AS BREWERY_NAME, 
    BR.CITY || ', ' || BR.STATE || ', ' || BR.COUNTRY AS ADDRESS, 
    ARRAY_AGG(T.TYPE) AS TYPE FROM BEER AS B 
    INNER JOIN BREWERY AS BR ON B.BREWERY = BR.ID 
    INNER JOIN BREWERY_TYPE AS BT ON BR.ID = BT.BREWERY
    INNER JOIN TYPE AS T ON BT.TYPE = T.ID 
    WHERE BR.COUNTRY <> 'US' AND NOT B.RETIRED GROUP BY (B.ID, BR.ID)) AS BEER_BREWERY
    WHERE 'Homebrew' = ANY(TYPE);""")
    print("%.3f" % (time.time() - current), "seconds to execute the query 4.")


def query5(connection):
    """
    This method is to fetch top-rated(based on look, smell, taste and feel) beers,
    which are available Year-round in NY
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("""SELECT B.NAME AS LIMITED_AVAIL_BEERS, BR.NAME AS BREWERY_NAME, BR.CITY AS CITY FROM BEER AS B
    INNER JOIN BREWERY AS BR ON B.BREWERY = BR.ID
    INNER JOIN AVAILABILITY AS A ON B.AVAILABILITY = A.ID 
    INNER JOIN REVIEWS AS R ON B.ID = R.BEER
    WHERE BR.COUNTRY = 'US' AND BR.STATE = 'NY' AND A.AVAILABILITY = 'Year-round' AND NOT B.RETIRED
    GROUP BY (B.ID, BR.ID) ORDER BY AVG((R.LOOK + R.SMELL + R.TASTE + R.FEEL) / 4) DESC LIMIT(5);""")
    print("%.3f" % (time.time() - current), "seconds to execute the query 5.")


def query6(connection):
    """
    This method is to fetch US breweries that brew more than 1000 top rated beer.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("""SELECT BR.NAME, BR.CITY || ', ' || BR.STATE || ', ' || BR.COUNTRY AS ADDRESS, 
    COUNT(CASE WHEN R.OVERALL > 4.5 THEN 1 END) AS OVERALL_QUALITY_BEERS
    FROM BREWERY AS BR INNER JOIN BEER AS B ON BR.ID = B.BREWERY
    INNER JOIN REVIEWS AS R ON B.ID = R.BEER 
    WHERE BR.COUNTRY = 'US' GROUP BY (BR.ID)
    HAVING COUNT(CASE WHEN R.OVERALL > 4.5 THEN 1 END) > 1000
    ORDER BY OVERALL_QUALITY_BEERS DESC;""")
    print("%.3f" % (time.time() - current), "seconds to execute the query 6.")


def query7(connection):
    """
    This method is to fetch style of beer that has the most number of beers registered
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("""SELECT S.STYLE,  COUNT(B.ID) FROM STYLE AS S 
    INNER JOIN BEER AS B ON S.ID = B.STYLE
    GROUP BY (S.ID) ORDER BY COUNT(B.ID) DESC LIMIT(1);""")
    print("%.3f" % (time.time() - current), "seconds to execute the query 7.")


def main():
    """
    The main program to run all the methods
    :return:
    """
    try:
        # Establishing the connection with PostgreSQL database
        # Change the parameters below accordingly
        connection = psycopg2.connect(database="project", user="postgres", \
                                      password="", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
        print("================================================")
        print("Database connection established successfully.")
        query1(connection)
        query2(connection)
        query3(connection)
        query4(connection)
        query5(connection)
        query6(connection)
        query6(connection)
        query7(connection)
    except psycopg2.DatabaseError as error:
        print("ERROR: " + str(error))
    finally:
        if(connection):
            # closing the cursor and the connection after every run.
            cursor.close()
            connection.close()
            print("Database connection is closed.")
            print("================================================")


# The following condition checks whether we are
# running as a script, in which case run the code.
# If the file is being imported, don't run the code.
if __name__ == '__main__':
    main()