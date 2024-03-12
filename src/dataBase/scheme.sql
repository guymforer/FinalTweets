-- CREATE DATABASE twitty;

\connect tweets

-- by likes and shares

CREATE TABLE tweets_by_likes (
    tweet_id bigint,
    author text,
    content text,
    country text,
    date_time timestamp without time zone,
    language text,
    latitude text,
    longitude text,
    number_of_likes int,
    number_of_shares int,
    parsed_content text[],
    PRIMARY KEY (number_of_likes, tweet_id)
) PARTITION BY RANGE (number_of_likes);

CREATE TABLE tweets_likes_low PARTITION OF tweets_by_likes
    FOR VALUES FROM (0) TO (1000);
CREATE TABLE tweets_likes_medium PARTITION OF tweets_by_likes
    FOR VALUES FROM (1000) TO (10000);
CREATE TABLE tweets_likes_high PARTITION OF tweets_by_likes
    FOR VALUES FROM (10000) TO (50000);
CREATE TABLE tweets_likes_very_high PARTITION OF tweets_by_likes
    FOR VALUES FROM (50000) TO (MAXVALUE);


CREATE TABLE tweets_by_share (
    tweet_id bigint,
    author text,
    content text,
    country text,
    date_time timestamp without time zone,
    language text,
    latitude text,
    longitude text,
    number_of_likes int,
    number_of_shares int,
    parsed_content text[],
    PRIMARY KEY (number_of_shares, tweet_id)
) PARTITION BY RANGE (number_of_shares);

CREATE TABLE tweets_shares_low PARTITION OF tweets_by_share
    FOR VALUES FROM (0) TO (400);
CREATE TABLE tweets_shares_medium PARTITION OF tweets_by_share
    FOR VALUES FROM (400) TO (1300);
CREATE TABLE tweets_shares_high PARTITION OF tweets_by_share
    FOR VALUES FROM (1300) TO (5300);
CREATE TABLE tweets_shares_very_high PARTITION OF tweets_by_share
    FOR VALUES FROM (5300) TO (MAXVALUE);    


-- by User

CREATE TABLE user_tweets (
    tweet_id BIGINT,
    author TEXT,
    content TEXT,
    country TEXT,
    date_time TIMESTAMP,
    language TEXT,
    latitude TEXT,
    longitude TEXT,
    number_of_likes INT,
    number_of_shares INT,
    parsed_content TEXT[],
    PRIMARY KEY (author, tweet_id)
) PARTITION BY HASH (author);

CREATE TABLE user_tweets_part1 PARTITION OF user_tweets FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE user_tweets_part2 PARTITION OF user_tweets FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE user_tweets_part3 PARTITION OF user_tweets FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE user_tweets_part4 PARTITION OF user_tweets FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- by word

CREATE TABLE tweets_by_word (
    tweet_id bigint,
    author text,
    content text,
    country text,
    date_time timestamp without time zone,
    language text,
    latitude text,
    longitude text,
    number_of_likes int,
    number_of_shares int,
    parsed_content text
) PARTITION BY RANGE (EXTRACT(YEAR FROM date_time));

-- Creating partitions for each year based on your distribution
CREATE TABLE tweets_by_date_2009 PARTITION OF tweets_by_word FOR VALUES FROM (MINVALUE) TO (2010);
CREATE TABLE tweets_by_date_2010 PARTITION OF tweets_by_word FOR VALUES FROM (2010) TO (2011);
CREATE TABLE tweets_by_date_2011 PARTITION OF tweets_by_word FOR VALUES FROM (2011) TO (2012);
CREATE TABLE tweets_by_date_2012 PARTITION OF tweets_by_word FOR VALUES FROM (2012) TO (2013);
CREATE TABLE tweets_by_date_2013 PARTITION OF tweets_by_word FOR VALUES FROM (2013) TO (2014);
CREATE TABLE tweets_by_date_2014 PARTITION OF tweets_by_word FOR VALUES FROM (2014) TO (2015);
CREATE TABLE tweets_by_date_2015 PARTITION OF tweets_by_word FOR VALUES FROM (2015) TO (2016);
CREATE TABLE tweets_by_date_2016 PARTITION OF tweets_by_word FOR VALUES FROM (2016) TO (2017);
CREATE TABLE tweets_by_date_2017 PARTITION OF tweets_by_word FOR VALUES FROM (2017) TO (MAXVALUE);


CREATE TABLE db_initialized (
    id INT PRIMARY KEY
);

INSERT INTO db_initialized(id) VALUES (1);


-- Utils

CREATE OR REPLACE FUNCTION time_format(origin timestamp)
RETURNS text AS $$
BEGIN
  RETURN to_char(origin, 'YYYY-MM-DD"T"HH24:MI:SS"Z"');
END;
$$  LANGUAGE plpgsql;
