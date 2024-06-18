import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from urllib.parse import quote

# Load the data
consumer_tweet_path = '/Users/kamrul.konok/Desktop/DigiScan360/sdm_joint_project/data/consumer_tweet.csv'
consumer_tweet = pd.read_csv(consumer_tweet_path)

# Define namespaces
ds = Namespace("http://example.org/digiscan360/")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Create an RDF graph
g = Graph()

def create_abox():
    for index, row in consumer_tweet.iterrows():
        tweet_uri = URIRef(f"http://example.org/digiscan360/tweet/{quote(str(row['tweet_id']))}")
        consumer_uri = URIRef(f"http://example.org/digiscan360/consumer/{quote(str(row['author_id']))}")

        # Add tweet instance
        g.add((tweet_uri, RDF.type, ds.Tweet))
        g.add((tweet_uri, ds.tweet_id, Literal(row['tweet_id'], datatype=XSD.string)))
        g.add((tweet_uri, ds.timestamp, Literal(row['timestamp'], datatype=XSD.dateTime)))
        g.add((tweet_uri, ds.brand_name, Literal(row['brand_name'], datatype=XSD.string)))
        g.add((tweet_uri, ds.impression_count, Literal(row['impression_count'], datatype=XSD.integer)))
        g.add((tweet_uri, ds.like_count, Literal(row['like_count'], datatype=XSD.integer)))
        g.add((tweet_uri, ds.reply_count, Literal(row['reply_count'], datatype=XSD.integer)))
        g.add((tweet_uri, ds.repost_count, Literal(row['repost_count'], datatype=XSD.integer)))
        g.add((tweet_uri, ds.quote_count, Literal(row['quote_count'], datatype=XSD.integer)))
        g.add((tweet_uri, ds.hashtags, Literal(row['hashtags'], datatype=XSD.string)))
        g.add((tweet_uri, ds.text, Literal(row['text'], datatype=XSD.string)))
        g.add((tweet_uri, ds.is_reply, Literal(row['is_reply'], datatype=XSD.boolean)))

        # Add consumer instance
        g.add((consumer_uri, RDF.type, ds.Consumer))
        g.add((consumer_uri, ds.author_id, Literal(row['author_id'], datatype=XSD.string)))
        g.add((consumer_uri, ds.screen_name, Literal(row['screen_name'], datatype=XSD.string)))
        g.add((consumer_uri, ds.user_followers_count, Literal(row['user_followers_count'], datatype=XSD.integer)))
        g.add((consumer_uri, ds.user_following_count, Literal(row['user_following_count'], datatype=XSD.integer)))
        g.add((consumer_uri, ds.verified_consumer, Literal(row['verified'], datatype=XSD.boolean)))

        # Add relationship between consumer and tweet
        g.add((consumer_uri, ds.tweets, tweet_uri))

    return g

if __name__ == "__main__":
    kg = create_abox()

    turtle = kg.serialize(format='turtle')
    kg.serialize(destination='abox_consumer_tweet.ttl', format='turtle')
    print(turtle)
