import pandas as pd
import rdflib
from rdflib.namespace import RDF, XSD
from rdflib import URIRef, Literal, Namespace

# Define namespaces
base_uri = URIRef("http://www.semanticweb.org/talha/ontologies/2024/3/rumour_detection/")
n = Namespace(base_uri)

# Load the RDF graph
g = rdflib.Graph()
g.parse("C:/Users/talha/Desktop/rumour_detection.ttl", format="ttl")  # Load your existing ontology structure if any

# Load CSV data
df = pd.read_csv("C:/Users/talha/Desktop/FakeNewsNet.csv")

# Iterate over the DataFrame and create individuals
for index, row in df.iterrows():
    if row.isna().any() or row.str.strip().eq('').any():  # Check if any block contains NA or empty string
        continue  # Skip this row if any block contains NA or empty string

    article_uri = n[f"Article_{index}"]
    source_uri = n[f"Source_{index}"]

    # Create Article individual
    g.add((article_uri, RDF.type, n.Article))
    g.add((article_uri, n.title, Literal(row['title'], datatype=XSD.string)))
    g.add((article_uri, n.url, Literal(row['news_url'], datatype=XSD.string)))
    g.add((article_uri, n.tweetCount, Literal(row['tweet_num'], datatype=XSD.integer)))
    g.add((article_uri, n.isReal, Literal(row['real'], datatype=XSD.boolean)))  # Use 'real' to match the CSV column

    # Create Source individual
    g.add((source_uri, RDF.type, n.Source))
    g.add((source_uri, n.sourceDomain, Literal(row['source_domain'], datatype=XSD.string)))

    # Link Article to Source
    g.add((article_uri, n.publishedBy, source_uri))

# Save the updated graph
g.serialize(destination="populated_ontology.ttl", format="ttl")
print("Ontology has been populated and saved.")
