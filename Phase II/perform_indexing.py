"""
CSCI-620: Group Project, Phase - II
Description: This file will perform indexing and call the methods of
re-run the queries and get the timing.
Authors:
Arpan Shah, Diptanu Sarkar, Lipisha Nitin Chaudhary, Ritaban Bhattacharya.
"""

# Importing python3 libraries for the project
import psycopg2
import interesting_queries as iq


def perform_indexing(connection):
    """
    This method will perform indexing in the database.
    :param connection:
    :return: None
    """
    cursor = connection.cursor()
    cursor.execute(open("index.sql", "r").read())
    print("INFO: Database indexing completed.")
    connection.commit()
    

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
        perform_indexing(connection)
        iq.query1(connection)
        iq.query2(connection)
        iq.query3(connection)
        iq.query4(connection)
        iq.query5(connection)
        iq.query6(connection)
        iq.query7(connection)
    except psycopg2.DatabaseError as error:
        # Rollback database to the previous state if any expection occurs.
        print ("INSERT FAILED: Rollback database to previous state. \nERROR: " + str(error))
        connection.rollback()
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