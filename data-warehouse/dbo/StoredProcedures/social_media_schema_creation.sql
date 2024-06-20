-- creating new dim_user table

CREATE TABLE new_dim_user (
    user_id BIGINT NOT NULL,
    name VARCHAR(255),
    username VARCHAR(255),
    created_at DATE,
    url VARCHAR(255),
    followers_count INT,
    record_date DATE
);

-- inserting data into the new dimension table

INSERT INTO new_dim_user (user_id, name, username, created_at, url, followers_count, record_date)
SELECT user_id, name, username, created_at, url, followers_count, record_date
FROM dim_user;

-- Creating new_dim_consumer table

CREATE TABLE new_dim_consumer (
    author_id BIGINT NOT NULL,
    screen_name VARCHAR(255),
    lang VARCHAR(255),
    brand_name VARCHAR(255)
);

INSERT INTO new_dim_consumer (author_id, screen_name, lang, brand_name)
SELECT author_id, screen_name, lang, brand_name
FROM dim_consumer;

-- Creating new_dim_facebook table

CREATE TABLE new_dim_facebook (
    page_id VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    username VARCHAR(255),
    contact_address VARCHAR(255),
    current_location VARCHAR(255)
);

INSERT INTO new_dim_facebook (page_id, name, username, contact_address, current_location)
SELECT page_id, name, username, contact_address, current_location
FROM dim_facebook;


-- Creating new_fact_user_tweet table
CREATE TABLE new_fact_user_tweet (
    id BIGINT NOT NULL,
    created_at DATE NOT NULL,
    followers_count INT,
    record_date DATE NOT NULL,
    friends_count INT,
    verified BIT
);

INSERT INTO new_fact_user_tweet (id, created_at, followers_count, record_date, friends_count, verified)
SELECT id, created_at, followers_count, record_date, friends_count, verified
FROM fact_user_tweet;

 select @@version

-- Creating new_fact_consumer_tweet
CREATE TABLE new_fact_consumer_tweet (
    tweet_id VARCHAR(255) NOT NULL,
    author_id BIGINT NOT NULL,
    in_reply_to_user_id BIGINT NOT NULL,
    timestamp DATETIME2(6) NOT NULL,
    text VARCHAR(8000),
    impression_count INT,
    like_count INT,
    reply_count INT,
    repost_count INT,
    quote_count INT,
    hashtags VARCHAR(8000),
    user_followers_count INT,
    user_following_count INT,
    verified BIT,
    tweet_date DATE
);

INSERT INTO new_fact_consumer_tweet (tweet_id, author_id, in_reply_to_user_id, timestamp, text, impression_count, like_count, reply_count, repost_count, quote_count, hashtags, user_followers_count, user_following_count, verified, tweet_date)
SELECT tweet_id, author_id, in_reply_to_user_id, timestamp, text, impression_count, like_count, reply_count, repost_count, quote_count, hashtags, user_followers_count, user_following_count, verified, CAST(timestamp AS DATE)
FROM fact_consumer_tweet;

-- Creating new_fact_facebook table
CREATE TABLE new_fact_facebook (
    page_id VARCHAR(255) NOT NULL,
    post_id VARCHAR(255) NOT NULL,
    created_time DATETIME2(6) NOT NULL,
    fans_count INT,
    followers_count INT,
    message VARCHAR(8000),
    shares INT,
    post_like_count INT,
    comment_like_count INT,
    reactions INT,
    comment_id VARCHAR(255),
    from_user_id VARCHAR(255) NOT NULL,
    comment VARCHAR(8000),
    verified BIT,
    created_date DATE
);

INSERT INTO new_fact_facebook (page_id, post_id, created_time, fans_count, followers_count, message, shares, post_like_count, comment_like_count, reactions, comment_id, from_user_id, comment, verified, created_date)
SELECT page_id, post_id, created_time, fans_count, followers_count, message, shares, post_like_count, comment_like_count, reactions, comment_id, from_user_id, comment, verified, CAST(created_time AS DATE)
FROM fact_facebook;


-- Dropping old tables

DROP TABLE IF EXISTS dim_user;
DROP TABLE IF EXISTS dim_consumer;
DROP TABLE IF EXISTS fact_user_tweet;
DROP TABLE IF EXISTS fact_consumer_tweet;
DROP TABLE IF EXISTS dim_facebook;
DROP TABLE IF EXISTS fact_facebook;


-- renaming the table
EXEC sp_rename 'new_dim_consumer', 'dim_consumer';
EXEC sp_rename 'new_dim_user', 'dim_user';
EXEC sp_rename 'new_fact_user_tweet', 'fact_user_tweet';
EXEC sp_rename 'new_fact_consumer_tweet', 'fact_consumer_tweet';
EXEC sp_rename 'new_dim_facebook', 'dim_facebook';
EXEC sp_rename 'new_fact_facebook', 'fact_facebook';


-- Add primary key to dim_user table
ALTER TABLE dim_user
ADD CONSTRAINT pk_dim_user_user_id PRIMARY KEY NONCLUSTERED (user_id) NOT ENFORCED;

-- Add primary key to dim_consumer table
ALTER TABLE dim_consumer
ADD CONSTRAINT pk_dim_consumer_author_id PRIMARY KEY NONCLUSTERED (author_id) NOT ENFORCED;

-- Add primary key to dim_facebook table
ALTER TABLE dim_facebook
ADD CONSTRAINT pk_dim_facebook_page_id PRIMARY KEY NONCLUSTERED (page_id) NOT ENFORCED;

-- Add foreign key to fact_user_tweet table
ALTER TABLE fact_user_tweet
ADD CONSTRAINT fk_fact_user_tweet_record_date FOREIGN KEY (record_date)
REFERENCES dim_time(date) NOT ENFORCED;

-- Add foreign key to fact_facebook table referencing dim_time table
ALTER TABLE fact_facebook
ADD CONSTRAINT fk_fact_facebook_created_date FOREIGN KEY (created_date)
REFERENCES dim_time(date) NOT ENFORCED;

-- Add foreign key to fact_consumer_tweet table referencing dim_time table
ALTER TABLE fact_consumer_tweet
ADD CONSTRAINT fk_fact_consumer_tweet_tweet_date FOREIGN KEY (tweet_date)
REFERENCES dim_time(date) NOT ENFORCED;


-- Add foreign key to fact_user_tweet table referencing dim_user table
ALTER TABLE fact_user_tweet
ADD CONSTRAINT fk_fact_user_tweet_user_id FOREIGN KEY (id)
REFERENCES dim_user(user_id) NOT ENFORCED;

-- Add foreign key to fact_facebook table referencing dim_facebook table
ALTER TABLE fact_facebook
ADD CONSTRAINT fk_fact_facebook_page_id FOREIGN KEY (page_id)
REFERENCES dim_facebook(page_id) NOT ENFORCED;

-- Add foreign key to fact_consumer_tweet table referencing dim_consumer table
ALTER TABLE fact_consumer_tweet
ADD CONSTRAINT fk_fact_consumer_tweet_author_id FOREIGN KEY (author_id)
REFERENCES dim_consumer(author_id) NOT ENFORCED;

