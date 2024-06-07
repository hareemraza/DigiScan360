import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace, RDF, XSD
from urllib.parse import quote

# Load the data
reviews_path = '/Users/kamrul.konok/Desktop/DigiScan360/sdm_joint_project/data/reviews.csv'
reviews = pd.read_csv(reviews_path, delimiter='|')

# Define namespaces
ds = Namespace("http://example.org/digiscan360/")
xsd = Namespace("http://www.w3.org/2001/XMLSchema#")

# Create an RDF graph
g = Graph()

def reviews_abox():
    for index, row in reviews.iterrows():
        review_uri = URIRef(f"http://example.org/digiscan360/review/{quote(str(row['review_id']))}")
        product_uri = URIRef(f"http://example.org/digiscan360/product/{quote(str(row['ProductID']))}")

        # Add review instance
        g.add((review_uri, RDF.type, ds.Review))
        g.add((review_uri, ds.review_id, Literal(row['review_id'], datatype=XSD.string)))
        g.add((review_uri, ds.title, Literal(row['title'], datatype=XSD.string)))
        g.add((review_uri, ds.body, Literal(row['body'], datatype=XSD.string)))
        g.add((review_uri, ds.num_helpful, Literal(row['num_helpful'], datatype=XSD.integer)))
        g.add((review_uri, ds.product_id, Literal(row['ProductID'], datatype=XSD.string)))
        g.add((review_uri, ds.date, Literal(row['date'], datatype=XSD.date)))
        g.add((review_uri, ds.sentiment, Literal(row['sentiment'], datatype=XSD.boolean)))
        g.add((review_uri, ds.summaries, Literal(row['summaries'], datatype=XSD.string)))

        # Add relationship to product
        g.add((review_uri, ds.reviews, product_uri))

    return g

if __name__ == "__main__":
    kg = reviews_abox()

    turtle = kg.serialize(format='turtle')
    kg.serialize(destination='abox_review.ttl', format='turtle')
    print(turtle)
