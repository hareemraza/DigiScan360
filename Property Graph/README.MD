# Property Graphs

This folder is used to implement product feature analysis for DigiScan360. This project leverages Neo4j to manage and analyze graph data efficiently. The instructions below will guide you on how to download, import, and analyze data using this project.

## Project Structure

- **scripts/load_data.cypher**: Cypher script to load data into the database.
- **queries/graph_analytics.cypher**: Cypher script containing analytical queries.
- **queries/graph_algorithms.cypher**: Cypher script containing graph algorithms.

**scripts** also contains some additional Python scripts. These are mainly used to generate product and review features from raw data. They don't have to be executed because the provided dataset already contains a sample of product and review features.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Neo4j](https://neo4j.com/download/)
- A Neo4j Desktop Project

## Getting Started

### Downloading the Data

1. **Download Data:**
   Download the dataset from the following link:

   [Download Data](https://drive.google.com/drive/folders/12zFUpn2E62k5qSyFZkOMOdy0eFtPneGR?usp=sharing) 

   You have to use UPC email address to access this data. Otherwise, you need to be granted access.

2. **Copy Data:**
   After downloading, copy the dataset file to the `import` directory of your Neo4j project. The `import` directory is typically located at:
   
   ```
   <neo4j_project_directory>/import/
   ```

### Loading the Data

1. **Open Neo4j Browser:**
   Launch the Neo4j Browser from your Neo4j Desktop.

2. **Run Load Data Script:**
   Execute the following script to load the data into your database. This script is located in the `scripts` directory of this project.

   ```
   scripts/load_data.cypher
   ```

### Running Analytical Queries and Algorithms

1. **Execute Analytical Queries:**
   Run the following scripts to perform graph analytics and algorithms. These scripts are located in the `queries` directory of this project.

   - Graph Analytics:
     ```
     queries/graph_analytics.cypher
     ```
   
   - Graph Algorithms:
     ```
     queries/graph_algorithms.cypher
     ```
