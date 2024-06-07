import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from urllib.parse import quote

# Load the data
products_path = '/Users/kamrul.konok/Desktop/DigiScan360/sdm_joint_project/data/products.csv'
products = pd.read_csv(products_path, delimiter='|')

# Define namespaces
ds = Namespace("http://example.org/digiscan360/")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Create an RDF graph
g = Graph()

def products_abox():
    for index, row in products.iterrows():
        product_uri = URIRef(f"http://example.org/digiscan360/product/{quote(str(row['ProductID']))}")
        brand_uri = URIRef(f"http://example.org/digiscan360/brand/{quote(str(row['SellerID']))}")
        seller_uri = URIRef(f"http://example.org/digiscan360/seller/{quote(str(row['SellerID']))}")

        # Add product instance
        g.add((product_uri, RDF.type, ds.Product))
        g.add((product_uri, ds.product_id, Literal(row['ProductID'], datatype=XSD.string)))
        g.add((product_uri, ds.date_accessed, Literal(row['date_accessed'], datatype=XSD.dateTime)))
        g.add((product_uri, ds.img_url, Literal(row['img_url'], datatype=XSD.anyURI)))
        g.add((product_uri, ds.num_reviews, Literal(row['num_reviews'], datatype=XSD.integer)))
        g.add((product_uri, ds.price, Literal(row['price'], datatype=XSD.float)))
        g.add((product_uri, ds.product_description, Literal(row['product_description'], datatype=XSD.string)))
        g.add((product_uri, ds.product_features, Literal(row['product_features'], datatype=XSD.string)))
        g.add((product_uri, ds.product_url, Literal(row['product_url'], datatype=XSD.anyURI)))
        g.add((product_uri, ds.rating, Literal(row['rating'], datatype=XSD.float)))
        g.add((product_uri, ds.title, Literal(row['title'], datatype=XSD.string)))
        g.add((product_uri, ds.rating_1, Literal(row['rating_1'], datatype=XSD.integer)))
        g.add((product_uri, ds.rating_2, Literal(row['rating_2'], datatype=XSD.integer)))
        g.add((product_uri, ds.rating_3, Literal(row['rating_3'], datatype=XSD.integer)))
        g.add((product_uri, ds.rating_4, Literal(row['rating_4'], datatype=XSD.integer)))
        g.add((product_uri, ds.rating_5, Literal(row['rating_5'], datatype=XSD.integer)))
        g.add((product_uri, ds.brand_name, Literal(row['SellerID'], datatype=XSD.string)))

        # Add seller instance
        g.add((seller_uri, RDF.type, ds.Seller))

        # Add relationship to brand
        g.add((product_uri, ds.belongsTo, seller_uri))
        g.add((seller_uri, ds.equivalentClass, brand_uri))

    return g

if __name__ == "__main__":
    kg = products_abox()

    turtle = kg.serialize(format='turtle')
    kg.serialize(destination='abox_product.ttl', format='turtle')
    print(turtle)
