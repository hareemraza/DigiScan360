from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD

# Define namespaces
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
ds = Namespace("http://example.org/digiscan360/")

# Create an empty graph
g = Graph()

# Add classes to the graph
g.add((ds.Tweet, RDF.type, RDFS.Class))
g.add((ds.Brand, RDF.type, RDFS.Class))

# Add properties for Tweet class
g.add((ds.tweet_id, RDF.type, RDF.Property))
g.add((ds.tweet_id, RDFS.domain, ds.Tweet))
g.add((ds.tweet_id, RDFS.range, XSD.string))

g.add((ds.author_id, RDF.type, RDF.Property))
g.add((ds.author_id, RDFS.domain, ds.Tweet))
g.add((ds.author_id, RDFS.range, XSD.string))

g.add((ds.screen_name, RDF.type, RDF.Property))
g.add((ds.screen_name, RDFS.domain, ds.Tweet))
g.add((ds.screen_name, RDFS.range, XSD.string))

g.add((ds.timestamp, RDF.type, RDF.Property))
g.add((ds.timestamp, RDFS.domain, ds.Tweet))
g.add((ds.timestamp, RDFS.range, XSD.dateTime))

g.add((ds.brand_name, RDF.type, RDF.Property))
g.add((ds.brand_name, RDFS.domain, ds.Tweet))
g.add((ds.brand_name, RDFS.range, XSD.string))

g.add((ds.impression_count, RDF.type, RDF.Property))
g.add((ds.impression_count, RDFS.domain, ds.Tweet))
g.add((ds.impression_count, RDFS.range, XSD.integer))

g.add((ds.like_count, RDF.type, RDF.Property))
g.add((ds.like_count, RDFS.domain, ds.Tweet))
g.add((ds.like_count, RDFS.range, XSD.integer))

g.add((ds.reply_count, RDF.type, RDF.Property))
g.add((ds.reply_count, RDFS.domain, ds.Tweet))
g.add((ds.reply_count, RDFS.range, XSD.integer))

g.add((ds.repost_count, RDF.type, RDF.Property))
g.add((ds.repost_count, RDFS.domain, ds.Tweet))
g.add((ds.repost_count, RDFS.range, XSD.integer))

g.add((ds.quote_count, RDF.type, RDF.Property))
g.add((ds.quote_count, RDFS.domain, ds.Tweet))
g.add((ds.quote_count, RDFS.range, XSD.integer))

g.add((ds.hashtags, RDF.type, RDF.Property))
g.add((ds.hashtags, RDFS.domain, ds.Tweet))
g.add((ds.hashtags, RDFS.range, XSD.string))

g.add((ds.user_followers_count, RDF.type, RDF.Property))
g.add((ds.user_followers_count, RDFS.domain, ds.Tweet))
g.add((ds.user_followers_count, RDFS.range, XSD.integer))

g.add((ds.user_following_count, RDF.type, RDF.Property))
g.add((ds.user_following_count, RDFS.domain, ds.Tweet))
g.add((ds.user_following_count, RDFS.range, XSD.integer))

g.add((ds.verified, RDF.type, RDF.Property))
g.add((ds.verified, RDFS.domain, ds.Tweet))
g.add((ds.verified, RDFS.range, XSD.boolean))

g.add((ds.text, RDF.type, RDF.Property))
g.add((ds.text, RDFS.domain, ds.Tweet))
g.add((ds.text, RDFS.range, XSD.string))

g.add((ds.is_reply, RDF.type, RDF.Property))
g.add((ds.is_reply, RDFS.domain, ds.Tweet))
g.add((ds.is_reply, RDFS.range, XSD.boolean))

# Add relationships
g.add((ds.mentionsBrand, RDF.type, RDF.Property))
g.add((ds.mentionsBrand, RDFS.domain, ds.Tweet))
g.add((ds.mentionsBrand, RDFS.range, ds.Brand))

# Serialize the graph to a file
g.serialize(destination='tbox_consumer_tweet.ttl', format='turtle')
print("TBox created and saved as 'tbox_consumer_tweet.ttl'")
