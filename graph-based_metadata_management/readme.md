# Knowledge Graph Metadata Management

## Overview

Welcome to the Knowledge Graph Metadata Management project! This repository contains the implementation of a graph-based metadata management system utilizing GraphDB and knowledge graphs. The project aims to provide an efficient and scalable solution for managing metadata in various domains.


## Folder Contents

This folder contains the following:

- `global_schema/`: Contains files related to the global schema of the knowledge graph.
    - `global_tbox.py`: Python script for TBox schema processing.
    - `tbox_global_schema.ttl`: Turtle file defining the global schema.

- `local_schema/`: Contains subfolders for different local schema types.
    - `brand_tweet/`: Local schema for brand tweets.
    - `consumer_tweet/`: Local schema for consumer tweets.
    - `products/`: Local schema for products.
    - `reviews/`: Local schema for reviews.

- `queries/`: Contains SPARQL query files.
- `LAV_mapping.py`: Python script for LAV mapping.

## Folder Structure

```plaintext
Knowledge Graph/
├── global_schema/
│   ├── global_tbox.py
│   └── tbox_global_schema.ttl
├── local_schema/
│   ├── brand_tweet/
│   ├── consumer_tweet/
│   ├── products/
│   └── reviews/
├── queries/
├── LAV_mapping.py
└── README.md
## Prerequisites

Before you begin, ensure you have met the following requirements:

- GraphDB
- Python (version 3.8 or later)
- Required Python packages (listed in requirements.txt)
- Access to the data on Google Drive (requires UPC email)

For data access, click on the [Data Access Link](https://drive.google.com/drive/u/1/folders/17zDEx-av2pHf23p_drZ63gttdV55ijDh) and sign in with your UPC email.

## Getting Started

To begin using this project, follow these steps:

1. Access the data by clicking on the [Data Access Link](https://drive.google.com/drive/u/1/folders/17zDEx-av2pHf23p_drZ63gttdV55ijDh) and sign in with your UPC email.
2. Once you have access to the data, you can start exploring and utilizing the knowledge graph metadata management system.

