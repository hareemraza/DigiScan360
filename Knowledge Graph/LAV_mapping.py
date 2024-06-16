# Function to execute a SPARQL CONSTRUCT query
from SPARQLWrapper import SPARQLWrapper, N3
from rdflib import Graph, Namespace, Literal, RDF, XSD
from datetime import datetime
import requests

GRAPHDB_BASE_URL = 'http://Konoks-MacBook-Pro.local:7200'
FEDERATED_REPO_URL = f'{GRAPHDB_BASE_URL}/repositories/federated'
GLOBAL_REPO_URL = f'{GRAPHDB_BASE_URL}/repositories/global_schema/statements'
METADATA_REPO_URL = f'{GRAPHDB_BASE_URL}/repositories/metadata/statements'

# Local repository URLs
LOCAL_CONSUMER_TWEET_REPO_URL = f'{GRAPHDB_BASE_URL}/repositories/local_consumer_tweet'
LOCAL_PRODUCT_DATA_REPO_URL = f'{GRAPHDB_BASE_URL}/repositories/local_product_data'
LOCAL_REVIEWS_DATA_REPO_URL = f'{GRAPHDB_BASE_URL}/repositories/local_reviews_data'
LOCAL_USER_TWEET_REPO_URL = f'{GRAPHDB_BASE_URL}/repositories/local_user_tweet'

meta = Namespace("http://example.org/digiscan360/metadata#")

# Function to execute a SPARQL CONSTRUCT query
def execute_construct_query(repo_url, query):
    sparql = SPARQLWrapper(repo_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(N3)
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        print(f"Error executing query on {repo_url}: {e}")
        return None

# Function to insert RDF data into a repository
def insert_data_into_repository(repo_url, rdf_data):
    headers = {'Content-Type': 'application/x-turtle'}
    response = requests.post(repo_url, data=rdf_data, headers=headers)
    if response.status_code == 204:
        print(f"Data inserted successfully into {repo_url}.")
    else:
        print(f"Error inserting data into {repo_url}: {response.text}")

# Function to create metadata instances for source tracking and audit trails
def create_metadata(entity, action, graph_uri):
    metadata_graph = Graph()
    metadata_graph.bind("meta", meta)
    timestamp = datetime.now().isoformat()
    source_instance = meta[entity]
    audit_instance = meta[f'audit_{entity}_{timestamp}']

    metadata_graph.add((source_instance, RDF.type, meta.Source))
    metadata_graph.add((source_instance, meta.sourceId, Literal(entity, datatype=XSD.string)))
    metadata_graph.add((source_instance, meta.sourceName, Literal(entity, datatype=XSD.string)))

    metadata_graph.add((audit_instance, RDF.type, meta.AuditTrail))
    metadata_graph.add((audit_instance, meta.timestamp, Literal(timestamp, datatype=XSD.dateTime)))
    metadata_graph.add((audit_instance, meta.action, Literal(action, datatype=XSD.string)))
    metadata_graph.add((audit_instance, meta.performedBy, Literal("Automated System", datatype=XSD.string)))
    metadata_graph.add((audit_instance, meta.relatedSource, source_instance))

    return metadata_graph.serialize(format='turtle')

# Define SPARQL CONSTRUCT queries for each entity
construct_queries = {
    'ConsumerTweet': """
        PREFIX global: <http://example.org/digiscan360/schema#>
        PREFIX local: <http://example.org/digiscan360/>

        CONSTRUCT {
        ?tweet a global:Tweet ;
                global:tweet_id ?tweet_id ;
                global:timestamp ?timestamp ;
                global:brand_name ?brand_name ;
                global:impression_count ?impression_count ;
                global:like_count ?like_count ;
                global:reply_count ?reply_count ;
                global:repost_count ?repost_count ;
                global:quote_count ?quote_count ;
                global:hashtags ?hashtags ;
                global:text ?text ;
                global:is_reply ?is_reply .

        ?consumer a global:Consumer ;
                    global:author_id ?author_id ;
                    global:screen_name ?screen_name ;
                    global:user_followers_count ?user_followers_count ;
                    global:user_following_count ?user_following_count ;
                    global:verified_consumer ?verified_consumer ;
                    global:tweets ?tweet .
        }
        WHERE {
            ?tweet a local:Tweet ;
                local:tweet_id ?tweet_id ;
                local:timestamp ?timestamp ;
                local:brand_name ?brand_name ;
                local:impression_count ?impression_count ;
                local:like_count ?like_count ;
                local:reply_count ?reply_count ;
                local:repost_count ?repost_count ;
                local:quote_count ?quote_count ;
                local:hashtags ?hashtags ;
                local:text ?text ;
                local:is_reply ?is_reply .

            ?consumer a local:Consumer ;
                    local:author_id ?author_id ;
                    local:screen_name ?screen_name ;
                    local:user_followers_count ?user_followers_count ;
                    local:user_following_count ?user_following_count ;
                    local:verified_consumer ?verified_consumer ;
                    local:tweets ?tweet .
        }

    """,
    'Product': """
    PREFIX global: <http://example.org/digiscan360/schema#>
    PREFIX local: <http://example.org/digiscan360/>

    CONSTRUCT {
      ?s a global:Product ;
         global:product_id ?product_id ;
         global:date_accessed ?date_accessed ;
         global:img_url ?img_url ;
         global:num_reviews ?num_reviews ;
         global:price ?price ;
         global:product_description ?product_description ;
         global:product_features ?product_features ;
         global:product_url ?product_url ;
         global:rating ?rating ;
         global:title ?title ;
         global:rating_1 ?rating_1 ;
         global:rating_2 ?rating_2 ;
         global:rating_3 ?rating_3 ;
         global:rating_4 ?rating_4 ;
         global:rating_5 ?rating_5 ;
         global:brand_name ?brand_name ;
         global:belongsTo ?belongsTo .
    }
    WHERE {
        ?s a local:Product ;
           local:product_id ?product_id ;
           local:date_accessed ?date_accessed ;
           local:img_url ?img_url ;
           local:num_reviews ?num_reviews ;
           local:price ?price ;
           local:product_description ?product_description ;
           local:product_features ?product_features ;
           local:product_url ?product_url ;
           local:rating ?rating ;
           local:title ?title ;
           local:rating_1 ?rating_1 ;
           local:rating_2 ?rating_2 ;
           local:rating_3 ?rating_3 ;
           local:rating_4 ?rating_4 ;
           local:rating_5 ?rating_5 ;
           local:brand_name ?brand_name ;
           local:belongsTo ?belongsTo .
    }
    """,
    'Review': """
    PREFIX global: <http://example.org/digiscan360/schema#>
    PREFIX local: <http://example.org/digiscan360/>

    CONSTRUCT {
      ?s a global:Review ;
         global:review_id ?review_id ;
         global:title ?title ;
         global:body ?body ;
         global:num_helpful ?num_helpful ;
         global:product_id ?product_id ;
         global:date ?date ;
         global:sentiment ?sentiment ;
         global:summaries ?summaries ;
         global:reviews ?reviews .
    }
    WHERE {
        ?s a local:Review ;
           local:review_id ?review_id ;
           local:title ?title ;
           local:body ?body ;
           local:num_helpful ?num_helpful ;
           local:product_id ?product_id ;
           local:date ?date ;
           local:sentiment ?sentiment ;
           local:summaries ?summaries ;
           local:reviews ?reviews .
    }
    """,
    'BrandTweet': """
        PREFIX global: <http://example.org/digiscan360/schema#>
        PREFIX local: <http://example.org/digiscan360/>

        CONSTRUCT {
        ?s a global:Brand ;
            global:user_id ?user_id ;
            global:name ?name ;
            global:username ?username ;
            global:created_at ?created_at ;
            global:url ?url ;
            global:followers_count ?followers_count ;
            global:record_date ?record_date ;
            global:friends_count ?friends_count ;
            global:verified ?verified ;
            global:mentionsBrand ?mentionsBrand .
        }
        WHERE {
            ?s a local:Brand ;
            local:user_id ?user_id ;
            local:name ?name ;
            local:username ?username ;
            local:created_at ?created_at ;
            local:url ?url ;
            local:followers_count ?followers_count ;
            local:record_date ?record_date ;
            local:friends_count ?friends_count ;
            local:verified ?verified ;
            local:mentionsBrand ?mentionsBrand .
        }
    """
}

# Map of local repository URLs
local_repositories = {
    'ConsumerTweet': LOCAL_CONSUMER_TWEET_REPO_URL,
    'Product': LOCAL_PRODUCT_DATA_REPO_URL,
    'Review': LOCAL_REVIEWS_DATA_REPO_URL,
    'BrandTweet': LOCAL_USER_TWEET_REPO_URL
}

# Execute each CONSTRUCT query and collect the results
rdf_data_collections = {}
for entity, query in construct_queries.items():
    repo_url = local_repositories[entity]
    print(f"Executing CONSTRUCT query for {entity} on {repo_url}...")
    rdf_data = execute_construct_query(repo_url, query)
    if rdf_data:
        rdf_data_collections[entity] = rdf_data
        print(f"Data for {entity} fetched successfully.")
    else:
        print(f"No results for {entity}.")

# Insert the constructed triples into the global repository along with metadata
for entity, rdf_data in rdf_data_collections.items():
    print(f"Inserting data for {entity} into the global repository...")
    insert_data_into_repository(GLOBAL_REPO_URL, rdf_data)
    metadata = create_metadata(entity, "Data Insertion", GLOBAL_REPO_URL)
    insert_data_into_repository(METADATA_REPO_URL, metadata)

print("Local to Global Mapping done using LAV with metadata tracking.")
