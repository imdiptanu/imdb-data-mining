"""
CSCI-620: Group Project, Phase - III
Description: This file will clean the dataset on relational tables of Phase I
schema.
(https://www.kaggle.com/ehallmar/beers-breweries-and-beer-reviews/version/2)
Authors:
Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
"""

# Importing python3 libraries for the project
import psycopg2


def clean_brewery_table(connection):
    """
    This table will clean the brewery table by adding city and state values
    to all breweries in the US that did not have them.
    :param connection:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(open("clean_brewery.sql", "r").read())
    print("INFO: Brewery table cleaning complete")
    connection.commit()


def clean_beer_table(connection):
    """
    This method will clean beer table - where beer id is different
    but all other attributes are same.
    :param connection:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(open("clean_beer.sql", "r").read())
    print("INFO: Beer table cleaning complete")
    connection.commit()


def clean_reviews_table(connection):
    """
    This method will clean reviews table where review is null and all
    other parameters are 0.
    :param connection:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(open("clean_reviews.sql", "r").read())
    print("INFO: Reviews table cleaning complete")
    connection.commit()


def main():
    """
    The main program
    :return: None
    """
    try:
        # connect to local PostgreSQL server.
        # please change database, user, password, host, port as needed.
        connection = psycopg2.connect(database="project", user="postgres", \
                                      password="", host="127.0.0.1", port="5432")
        # turn off the auto commit for the database
        connection.autocommit = False
        cursor = connection.cursor()
        print("Database connection established successfully.")
        # clean brewery table
        clean_brewery_table(connection)
        clean_beer_table(connection)
        clean_reviews_table(connection)
    except psycopg2.DatabaseError as error:
        print("INSERT FAILED: Rollback database to previous state. \nERROR: " + str(error))
        connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Database connection is closed.")


# The following condition checks whether we are
# running as a script, in which case run the code.
# If the file is being imported, don't run the code.
if __name__ == '__main__':
    main()