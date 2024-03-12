import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
import os
import ast
import numpy as np

def make_list(row):
    """
    Converts a string representation of a list into an actual Python list object.
    If conversion fails, returns an empty list.

    Parameters:
    - row (str): A string representation of a list.

    Returns:
    - list: The converted list or an empty list on failure.
    """
    try:
        return ast.literal_eval(row)
    except ValueError:
        return []

def insert_data():
    """
    Loads tweet data from a CSV file, preprocesses it, and then inserts it into a PostgreSQL database.
    It creates several tables based on different criteria such as likes, shares, and content partitioning.
    """
    current = None
    connect = None
    try:
        # Fetch database connection parameters from environment variables or use defaults
        password = "MosheForer97"
        user = "postgres"
        host = "postgres-service"
        # Establish connection to the PostgreSQL database
        connect = psycopg2.connect(
            dbname='tweets',
            user=user,
            host=host,
            password=password
        )
        current = connect.cursor()

        # Read tweet data from CSV, handling missing values
        tweets_ = pd.read_csv('tweets_df.csv', delimiter='\t')
        tweets_.replace({np.nan: None}, inplace=True)

        # Partition tweets by words for detailed analysis
        tweets_['parsed_content'] = tweets_['parsed_content'].apply(make_list)
        tweets_partitioned_by_word = tweets_.explode('parsed_content')
        tweets_partitioned_by_word.dropna(subset=["parsed_content"], inplace=True)

        # Prepare raw data tuples for bulk insertion into PostgreSQL
        twitter_tweets = list(tweets_[['tweet_id', 'author', 'content', 'country', 'date_time', 'language', 'latitude', 'longitude', 'number_of_likes', 'number_of_shares', 'parsed_content']].itertuples(index=False, name=None))

        print('Starting with tables creation.')

        # Insertion queries for different tables based on the tweet data
        insert_queries = {
            "tweets_by_likes": """INSERT INTO tweets_by_likes (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;""",
            "tweets_by_share": """INSERT INTO tweets_by_share (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;""",
            "user_tweets": """INSERT INTO user_tweets (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;""",
            "tweets_by_word": """INSERT INTO tweets_by_word (tweet_id, author, content, country, date_time, language, latitude, longitude, number_of_likes, number_of_shares, parsed_content) VALUES %s;"""
        }

        # Execute insert queries for each table
        for table_name, query in insert_queries.items():
            if table_name == "tweets_by_word":
                raw_data = list(tweets_partitioned_by_word[['tweet_id', 'author', 'content', 'country', 'date_time', 'language', 'latitude', 'longitude', 'number_of_likes', 'number_of_shares', 'parsed_content']].itertuples(index=False, name=None))
                execute_values(current, query, raw_data)
            else:
                execute_values(current, query, twitter_tweets)
            print(f'Finished creating {table_name}')

        # Mark the database as digested
        current.execute("""CREATE TABLE db_digested (id INT PRIMARY KEY);""")
        current.execute("""INSERT INTO db_digested(id) VALUES (1);""")

        # Commit the transaction to save changes
        connect.commit()
        print('Finished creating all tables and completing data digestion.')

    except Exception as e:
        # Handle any errors by rolling back the transaction
        if connect is not None:
            connect.rollback()
        print(f"error: {e}")
        raise
    finally:
        # Ensure database connections are closed
        if current is not None:
            current.close()
        if connect is not None:
            connect.close()

if __name__ == "__main__":
    insert_data()
