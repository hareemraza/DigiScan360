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
g.add((ds.Review, RDF.type, RDFS.Class))
g.add((ds.Product, RDF.type, RDFS.Class))

# Add properties for Review class
g.add((ds.review_id, RDF.type, RDF.Property))
g.add((ds.review_id, RDFS.domain, ds.Review))
g.add((ds.review_id, RDFS.range, XSD.string))

g.add((ds.title, RDF.type, RDF.Property))
g.add((ds.title, RDFS.domain, ds.Review))
g.add((ds.title, RDFS.range, XSD.string))

g.add((ds.body, RDF.type, RDF.Property))
g.add((ds.body, RDFS.domain, ds.Review))
g.add((ds.body, RDFS.range, XSD.string))

g.add((ds.num_helpful, RDF.type, RDF.Property))
g.add((ds.num_helpful, RDFS.domain, ds.Review))
g.add((ds.num_helpful, RDFS.range, XSD.integer))

g.add((ds.product_id, RDF.type, RDF.Property))
g.add((ds.product_id, RDFS.domain, ds.Review))
g.add((ds.product_id, RDFS.range, XSD.string))

g.add((ds.date, RDF.type, RDF.Property))
g.add((ds.date, RDFS.domain, ds.Review))
g.add((ds.date, RDFS.range, XSD.date))

g.add((ds.sentiment, RDF.type, RDF.Property))
g.add((ds.sentiment, RDFS.domain, ds.Review))
g.add((ds.sentiment, RDFS.range, XSD.boolean))

g.add((ds.summaries, RDF.type, RDF.Property))
g.add((ds.summaries, RDFS.domain, ds.Review))
g.add((ds.summaries, RDFS.range, XSD.string))

# Add relationships
g.add((ds.reviews, RDF.type, RDF.Property))
g.add((ds.reviews, RDFS.domain, ds.Review))
g.add((ds.reviews, RDFS.range, ds.Product))

# Serialize the graph to a file
g.serialize(destination='tbox_review.ttl', format='turtle')
print("TBox created and saved as 'tbox_review.ttl'")
