import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from urllib.parse import quote

# Load the data
user_tweet_path = '/Users/kamrul.konok/Desktop/sdm_joint_project/data/user_tweet.csv'
user_tweet = pd.read_csv(user_tweet_path)

# Define namespaces
ds = Namespace("http://example.org/digiscan360/")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Create an RDF graph
g = Graph()

def users():
    for index, row in user_tweet.iterrows():
        user_uri = URIRef(f"http://example.org/digiscan360/user/{quote(str(row['id']))}")

        # Add user instance
        g.add((user_uri, RDF.type, ds.User))
        g.add((user_uri, ds.user_id, Literal(row['id'], datatype=XSD.string)))
        g.add((user_uri, ds.name, Literal(row['name'], datatype=XSD.string)))
        g.add((user_uri, ds.username, Literal(row['username'], datatype=XSD.string)))
        g.add((user_uri, ds.created_at, Literal(row['created_at'], datatype=XSD.dateTime)))
        g.add((user_uri, ds.url, Literal(row['url'], datatype=XSD.anyURI)))
        g.add((user_uri, ds.followers_count, Literal(row['followers_count'], datatype=XSD.integer)))
        g.add((user_uri, ds.record_date, Literal(row['record_date'], datatype=XSD.dateTime)))
        g.add((user_uri, ds.friends_count, Literal(row['friends_count'], datatype=XSD.integer)))
        g.add((user_uri, ds.verified, Literal(row['verified'], datatype=XSD.boolean)))

    return g

if __name__ == "__main__":
    kg = users()

    turtle = kg.serialize(format='turtle')
    kg.serialize(destination='abox_user_tweet.ttl', format='turtle')
    print(turtle)
