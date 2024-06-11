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
g.add((ds.Brand, RDF.type, RDFS.Class))

# Add properties for Brand class
g.add((ds.user_id, RDF.type, RDF.Property))
g.add((ds.user_id, RDFS.domain, ds.Brand))
g.add((ds.user_id, RDFS.range, XSD.string))

g.add((ds.name, RDF.type, RDF.Property))
g.add((ds.name, RDFS.domain, ds.Brand))
g.add((ds.name, RDFS.range, XSD.string))

g.add((ds.username, RDF.type, RDF.Property))
g.add((ds.username, RDFS.domain, ds.Brand))
g.add((ds.username, RDFS.range, XSD.string))

g.add((ds.created_at, RDF.type, RDF.Property))
g.add((ds.created_at, RDFS.domain, ds.Brand))
g.add((ds.created_at, RDFS.range, XSD.dateTime))

g.add((ds.url, RDF.type, RDF.Property))
g.add((ds.url, RDFS.domain, ds.Brand))
g.add((ds.url, RDFS.range, XSD.anyURI))

g.add((ds.followers_count, RDF.type, RDF.Property))
g.add((ds.followers_count, RDFS.domain, ds.Brand))
g.add((ds.followers_count, RDFS.range, XSD.integer))

g.add((ds.record_date, RDF.type, RDF.Property))
g.add((ds.record_date, RDFS.domain, ds.Brand))
g.add((ds.record_date, RDFS.range, XSD.dateTime))

g.add((ds.friends_count, RDF.type, RDF.Property))
g.add((ds.friends_count, RDFS.domain, ds.Brand))
g.add((ds.friends_count, RDFS.range, XSD.integer))

g.add((ds.verified, RDF.type, RDF.Property))
g.add((ds.verified, RDFS.domain, ds.Brand))
g.add((ds.verified, RDFS.range, XSD.boolean))

# Add relationships
g.add((ds.mentionsBrand, RDF.type, RDF.Property))
g.add((ds.mentionsBrand, RDFS.domain, ds.Tweet))
g.add((ds.mentionsBrand, RDFS.range, ds.Brand))

# Serialize the graph to a file
g.serialize(destination='tbox_brand_tweet.ttl', format='turtle')
print("TBox created and saved as 'tbox_user_tweet.ttl'")
