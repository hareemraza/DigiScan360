// PageRank for Influential Features

CALL gds.graph.project(
  'productFeatureGraph',
  ['Review', 'Feature', 'Product'],
  {
    HAS_REVIEW: {
      type: 'HAS_REVIEW',
      properties: [ 'Rating', 'NumHelpful', 'Sentiment']
    },
    TALKS_ABOUT: {
      type: 'TALKS_ABOUT',
      properties: ['Sentiment']
    }
  }
) YIELD graphName, nodeCount, relationshipCount;
CALL gds.pageRank.write('productFeatureGraph', {
  writeProperty: 'pagerank',
  relationshipWeightProperty: 'Sentiment'
})
YIELD nodePropertiesWritten, ranIterations, didConverge;
MATCH (f:Feature)
RETURN f.FeatureName as FeatureName, ROUND(f.pagerank, 2) as PageRank
ORDER BY f.pagerank DESC
LIMIT 10;



// Node Similarity for Product Comparison
CALL gds.graph.project(
    'productFeatureGraph',
    ['Product', 'Feature'],
    {
        HAS_FEATURE: {
            type: 'HAS_FEATURE',
            orientation: 'UNDIRECTED'
        }
    }
)
YIELD graphName, nodeCount, relationshipCount;
CALL gds.nodeSimilarity.stream('productFeatureGraph')
YIELD node1, node2, similarity
MATCH (p1:Product) WHERE id(p1) = node1
MATCH (p2:Product) WHERE id(p2) = node2
RETURN p1.Title AS Product1, p2.Title AS Product2, similarity
ORDER BY similarity DESC
LIMIT 10;


