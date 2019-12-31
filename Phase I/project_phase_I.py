"""
CSCI-620: Group Project, Phase - I
Description: This file will load the Beers, Breweries, and Beer Reviews dataset
(https://www.kaggle.com/ehallmar/beers-breweries-and-beer-reviews/version/2)
into PostgreSQL database.
Authors: 
Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
"""

# Importing python3 libraries for the project
import time
import csv
import psycopg2
import sys

# To increase system field size to maximum
csv.field_size_limit(sys.maxsize)


def create_temp_tables(connection):
    """
    This table will create the temporary tables in the database.
    :param connection:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(open("create_temp_tables.sql", "r").read())
    print("INFO: Temporary tables are created.")
    connection.commit()
    
    
def load_temp_beer(connection):
    """
    This table will load beers.csv to the database temporarily.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    with open('beers.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            # removing unwanted space
            row[5] = row[5].strip()
            row[6] = row[6].strip()
            # setting the 'abv' value to 0.0 if not provided in the dataset
            if row[7] is "":
                row[7] = 0.0
            cursor.execute("INSERT INTO temp_beers VALUES"
                           "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
    connection.commit()
    print((time.time() - current) // 60, " minutes to load temp_beers table.")


def load_temp_breweries(connection):
    """
    This table will load breweries.csv to the database temporarily.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    with open('breweries.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            # To make 'types' of the breweries an array
            row[6] = row[6].split(", ")
            cursor.execute("INSERT INTO temp_breweries VALUES"
                           "(%s, %s, %s, %s, %s, %s, %s)", row)
    connection.commit()
    print((time.time() - current) // 60, " minutes to load temp_breweries table.")


def load_temp_reviews(connection):
    """
    This table will load reviews.csv to the database temporarily.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    with open('reviews.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            # removing unwanted space
            row[3] = row[3].strip()
            # setting the 'look', 'smell', 'taste', 'feel', 'overall', 'score' 
            #   value to 0.0 if not provided in the dataset 
            for index in range(4,10):
                if row[index] == "":
                    row[index] = 0.0
            cursor.execute("INSERT INTO temp_reviews"
                           "(beer_id, username, date, text, look, smell, taste, feel, overall, score)"
                           " VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
    connection.commit()
    print((time.time() - current) // 60, " minutes to load temp_reviews table.")


def create_schema_tables(connection):
    """
    This table will create the temporary tables in the database.
    :param connection:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(open("create_schema_tables.sql", "r").read())
    print("INFO: Schema tables are created.")
    connection.commit()
    
    
def load_brewery(connection):
    """
    This table will load brewery table to the database.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO brewery SELECT id, name, city, state, country FROM temp_breweries")
    connection.commit()
    print((time.time() - current) // 60, " minutes to load brewery table.")


def load_style(connection):
    """
    This table will load style table to the database.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO style(style) SELECT DISTINCT style FROM temp_beers GROUP BY style")
    connection.commit()
    print((time.time() - current) // 60, " minutes to load style table.")


def load_type(connection):
    """
    This table will load type table to the database.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO type(type) SELECT DISTINCT unnest(types) FROM temp_breweries "
                   "GROUP BY types")
    connection.commit()
    print((time.time() - current) // 60, " minutes to load type table.")


def load_availability(connection):
    """
    This table will load availability table to the database.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO availability(availability) "
                   "SELECT DISTINCT availability FROM temp_beers GROUP BY availability")
    connection.commit()
    print((time.time() - current) // 60, " minutes to load availability table.")


def load_brewery_type(connection):
    """
    This table will load brewery type table to the database.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO brewery_type "
                   "SELECT b.id, t.id FROM temp_breweries as b, type AS t WHERE t.type = ANY(types)")
    connection.commit()
    print((time.time() - current) // 60, " minutes to load brewery type table.")


def load_beer(connection):
    """
    This table will load beer table to the database.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO beer "
                   "SELECT b.id, b.name, br.id, s.id, a.id, b.abv, b.retired "
                   "FROM temp_beers AS b, temp_breweries AS br, style AS s, availability AS a "
                   "WHERE b.brewery_id = br.id AND b.style = s.style AND b.availability = a.availability")
    connection.commit()
    print((time.time() - current) // 60, " minutes to load beer table.")


def load_review(connection):
    """
    This table will load reviews table to the database.
    :param connection:
    :return: None
    """
    current = time.time()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO reviews "
                   "SELECT r.beer_id, r.username, r.date, r.text, r.look, r.smell, r.taste, r.feel, r.overall "
                   "FROM temp_reviews AS r, beer AS b WHERE  r.beer_id = b.id")
    connection.commit()
    print((time.time() - current) // 60, " minutes to load reviews table.")
    
    
def drop_temp_tables(connection):
    """
    This table will drop the temporary tables from the database.
    :param connection:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(open("drop_temp_tables.sql", "r").read())
    print("INFO: Temporary tables are dropped.")
    connection.commit()


def main():
    """
    The main program
    :return: None
    """
    total = time.time()
    try:
        # connect to local PostgreSQL server.
        # please change database, user, password, host, port as needed.
        connection = psycopg2.connect(database = "project", user = "postgres", \
                                      password = "", host = "127.0.0.1", port = "5432")
        # turn off the auto commit for the database
        connection.autocommit = False
        cursor = connection.cursor()
        print("================================================")
        print("Database connection established successfully.")
        print("================================================")
        # create temporary tables and load them from dataset.
        create_temp_tables(connection)
        load_temp_beer(connection)
        load_temp_breweries(connection)
        load_temp_reviews(connection)
        # create schema tables for the project and load the tables
        #   using the temporary tables.
        create_schema_tables(connection)
        load_brewery(connection)
        load_style(connection)
        load_type(connection)
        load_availability(connection)
        load_brewery_type(connection)
        load_beer(connection)
        load_review(connection)
        # drop temporary tables
        drop_temp_tables(connection)
        print("All Data inserted successfully.")
        print("================================================")
        print((time.time() - total) // 60, " minutes to load complete Beer Breweries dataset to the database.")        
    except psycopg2.DatabaseError as error:
        # incase of any error rollback database to the previous state
        print ("INSERT FAILED: Rollback database to previous state. \nERROR: " + str(error))
        connection.rollback() 
    finally:
        if connection:
            # close curson and connection
            cursor.close()
            connection.close()
            print("================================================")
            print("Database connection is closed.")
            print("================================================")
        
# The following condition checks whether we are
# running as a script, in which case run the code.
# If the file is being imported, don't run the code.
if __name__ == '__main__':
    main()