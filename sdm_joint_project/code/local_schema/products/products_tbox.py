from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, OWL

# Define namespaces
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
ds = Namespace("http://example.org/digiscan360/")

# Create an empty graph
g = Graph()

# Add classes to the graph
g.add((ds.Product, RDF.type, RDFS.Class))
g.add((ds.Brand, RDF.type, RDFS.Class))
g.add((ds.Seller, RDF.type, RDFS.Class))

# Add properties for Product class
g.add((ds.product_id, RDF.type, RDF.Property))
g.add((ds.product_id, RDFS.domain, ds.Product))
g.add((ds.product_id, RDFS.range, XSD.string))

g.add((ds.date_accessed, RDF.type, RDF.Property))
g.add((ds.date_accessed, RDFS.domain, ds.Product))
g.add((ds.date_accessed, RDFS.range, XSD.dateTime))

g.add((ds.img_url, RDF.type, RDF.Property))
g.add((ds.img_url, RDFS.domain, ds.Product))
g.add((ds.img_url, RDFS.range, XSD.anyURI))

g.add((ds.num_reviews, RDF.type, RDF.Property))
g.add((ds.num_reviews, RDFS.domain, ds.Product))
g.add((ds.num_reviews, RDFS.range, XSD.integer))

g.add((ds.price, RDF.type, RDF.Property))
g.add((ds.price, RDFS.domain, ds.Product))
g.add((ds.price, RDFS.range, XSD.float))

g.add((ds.product_description, RDF.type, RDF.Property))
g.add((ds.product_description, RDFS.domain, ds.Product))
g.add((ds.product_description, RDFS.range, XSD.string))

g.add((ds.product_features, RDF.type, RDF.Property))
g.add((ds.product_features, RDFS.domain, ds.Product))
g.add((ds.product_features, RDFS.range, XSD.string))

g.add((ds.product_url, RDF.type, RDF.Property))
g.add((ds.product_url, RDFS.domain, ds.Product))
g.add((ds.product_url, RDFS.range, XSD.anyURI))

g.add((ds.rating, RDF.type, RDF.Property))
g.add((ds.rating, RDFS.domain, ds.Product))
g.add((ds.rating, RDFS.range, XSD.float))

g.add((ds.title, RDF.type, RDF.Property))
g.add((ds.title, RDFS.domain, ds.Product))
g.add((ds.title, RDFS.range, XSD.string))

g.add((ds.rating_1, RDF.type, RDF.Property))
g.add((ds.rating_1, RDFS.domain, ds.Product))
g.add((ds.rating_1, RDFS.range, XSD.integer))

g.add((ds.rating_2, RDF.type, RDF.Property))
g.add((ds.rating_2, RDFS.domain, ds.Product))
g.add((ds.rating_2, RDFS.range, XSD.integer))

g.add((ds.rating_3, RDF.type, RDF.Property))
g.add((ds.rating_3, RDFS.domain, ds.Product))
g.add((ds.rating_3, RDFS.range, XSD.integer))

g.add((ds.rating_4, RDF.type, RDF.Property))
g.add((ds.rating_4, RDFS.domain, ds.Product))
g.add((ds.rating_4, RDFS.range, XSD.integer))

g.add((ds.rating_5, RDF.type, RDF.Property))
g.add((ds.rating_5, RDFS.domain, ds.Product))
g.add((ds.rating_5, RDFS.range, XSD.integer))

g.add((ds.brand_name, RDF.type, RDF.Property))
g.add((ds.brand_name, RDFS.domain, ds.Product))
g.add((ds.brand_name, RDFS.range, XSD.string))

# Add relationships
g.add((ds.belongsTo, RDF.type, RDF.Property))
g.add((ds.belongsTo, RDFS.domain, ds.Product))
g.add((ds.belongsTo, RDFS.range, ds.Seller))

g.add((ds.Brand, OWL.equivalentClass, ds.Seller))

# Serialize the graph to a file
g.serialize(destination='tbox_product.ttl', format='turtle')
print("TBox created and saved as 'tbox_product.ttl'")
