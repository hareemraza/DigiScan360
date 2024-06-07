from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, OWL

# Define namespaces
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
ds = Namespace("http://example.org/digiscan360/")

# Create an empty graph
g = Graph()

# Add classes to the graph
g.add((ds.User, RDF.type, RDFS.Class))
g.add((ds.Tweet, RDF.type, RDFS.Class))
g.add((ds.Brand, RDF.type, RDFS.Class))
g.add((ds.Seller, RDF.type, RDFS.Class))
g.add((ds.Product, RDF.type, RDFS.Class))
g.add((ds.Review, RDF.type, RDFS.Class))

# Add properties for User class
g.add((ds.user_id, RDF.type, RDF.Property))
g.add((ds.user_id, RDFS.domain, ds.User))
g.add((ds.user_id, RDFS.range, XSD.string))

g.add((ds.name, RDF.type, RDF.Property))
g.add((ds.name, RDFS.domain, ds.User))
g.add((ds.name, RDFS.range, XSD.string))

g.add((ds.username, RDF.type, RDF.Property))
g.add((ds.username, RDFS.domain, ds.User))
g.add((ds.username, RDFS.range, XSD.string))

g.add((ds.created_at, RDF.type, RDF.Property))
g.add((ds.created_at, RDFS.domain, ds.User))
g.add((ds.created_at, RDFS.range, XSD.dateTime))

g.add((ds.url, RDF.type, RDF.Property))
g.add((ds.url, RDFS.domain, ds.User))
g.add((ds.url, RDFS.range, XSD.anyURI))

g.add((ds.followers_count, RDF.type, RDF.Property))
g.add((ds.followers_count, RDFS.domain, ds.User))
g.add((ds.followers_count, RDFS.range, XSD.integer))

g.add((ds.record_date, RDF.type, RDF.Property))
g.add((ds.record_date, RDFS.domain, ds.User))
g.add((ds.record_date, RDFS.range, XSD.dateTime))

g.add((ds.friends_count, RDF.type, RDF.Property))
g.add((ds.friends_count, RDFS.domain, ds.User))
g.add((ds.friends_count, RDFS.range, XSD.integer))

g.add((ds.verified, RDF.type, RDF.Property))
g.add((ds.verified, RDFS.domain, ds.User))
g.add((ds.verified, RDFS.range, XSD.boolean))

# Add properties for Tweet class
g.add((ds.tweet_id, RDF.type, RDF.Property))
g.add((ds.tweet_id, RDFS.domain, ds.Tweet))
g.add((ds.tweet_id, RDFS.range, XSD.string))

g.add((ds.tweet_text, RDF.type, RDF.Property))
g.add((ds.tweet_text, RDFS.domain, ds.Tweet))
g.add((ds.tweet_text, RDFS.range, XSD.string))

g.add((ds.tweet_date, RDF.type, RDF.Property))
g.add((ds.tweet_date, RDFS.domain, ds.Tweet))
g.add((ds.tweet_date, RDFS.range, XSD.dateTime))

# Add properties for Brand class
g.add((ds.brand_id, RDF.type, RDF.Property))
g.add((ds.brand_id, RDFS.domain, ds.Brand))
g.add((ds.brand_id, RDFS.range, XSD.string))

g.add((ds.brand_name, RDF.type, RDF.Property))
g.add((ds.brand_name, RDFS.domain, ds.Brand))
g.add((ds.brand_name, RDFS.range, XSD.string))

# Add properties for Seller class
g.add((ds.seller_id, RDF.type, RDF.Property))
g.add((ds.seller_id, RDFS.domain, ds.Seller))
g.add((ds.seller_id, RDFS.range, XSD.string))

g.add((ds.seller_name, RDF.type, RDF.Property))
g.add((ds.seller_name, RDFS.domain, ds.Seller))
g.add((ds.seller_name, RDFS.range, XSD.string))

# Add properties for Product class
g.add((ds.product_id, RDF.type, RDF.Property))
g.add((ds.product_id, RDFS.domain, ds.Product))
g.add((ds.product_id, RDFS.range, XSD.string))

g.add((ds.product_name, RDF.type, RDF.Property))
g.add((ds.product_name, RDFS.domain, ds.Product))
g.add((ds.product_name, RDFS.range, XSD.string))

g.add((ds.product_price, RDF.type, RDF.Property))
g.add((ds.product_price, RDFS.domain, ds.Product))
g.add((ds.product_price, RDFS.range, XSD.float))

g.add((ds.product_description, RDF.type, RDF.Property))
g.add((ds.product_description, RDFS.domain, ds.Product))
g.add((ds.product_description, RDFS.range, XSD.string))

g.add((ds.product_url, RDF.type, RDF.Property))
g.add((ds.product_url, RDFS.domain, ds.Product))
g.add((ds.product_url, RDFS.range, XSD.anyURI))

# Add properties for Review class
g.add((ds.review_id, RDF.type, RDF.Property))
g.add((ds.review_id, RDFS.domain, ds.Review))
g.add((ds.review_id, RDFS.range, XSD.string))

g.add((ds.review_title, RDF.type, RDF.Property))
g.add((ds.review_title, RDFS.domain, ds.Review))
g.add((ds.review_title, RDFS.range, XSD.string))

g.add((ds.review_body, RDF.type, RDF.Property))
g.add((ds.review_body, RDFS.domain, ds.Review))
g.add((ds.review_body, RDFS.range, XSD.string))

g.add((ds.review_rating, RDF.type, RDF.Property))
g.add((ds.review_rating, RDFS.domain, ds.Review))
g.add((ds.review_rating, RDFS.range, XSD.integer))

g.add((ds.review_date, RDF.type, RDF.Property))
g.add((ds.review_date, RDFS.domain, ds.Review))
g.add((ds.review_date, RDFS.range, XSD.dateTime))

# Add relationships
g.add((ds.tweets, RDF.type, RDF.Property))
g.add((ds.tweets, RDFS.domain, ds.User))
g.add((ds.tweets, RDFS.range, ds.Tweet))

g.add((ds.mentionsBrand, RDF.type, RDF.Property))
g.add((ds.mentionsBrand, RDFS.domain, ds.Tweet))
g.add((ds.mentionsBrand, RDFS.range, ds.Brand))

g.add((ds.belongsTo, RDF.type, RDF.Property))
g.add((ds.belongsTo, RDFS.domain, ds.Product))
g.add((ds.belongsTo, RDFS.range, ds.Seller))

g.add((ds.Brand, OWL.equivalentClass, ds.Seller))

g.add((ds.reviews, RDF.type, RDF.Property))
g.add((ds.reviews, RDFS.domain, ds.Review))
g.add((ds.reviews, RDFS.range, ds.Product))

# Serialize the graph to a file
g.serialize(destination='tbox_global_schema.ttl', format='turtle')