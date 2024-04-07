# DigiScan360

## Installation

Ensure you have Python version 3.9 or higher installed, then install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

The data collection process consists of three main steps:

### 1. Collect Data for Amazon

Run the following command to collect data from Amazon:

```
python -m data_collection.amazon_collector
```

### 2. Collect Data for MediaMarkt

Execute the command below to gather data from MediaMarkt:

```
python -m data_collection.mediamarkt_collector
```

### 3. Upload Data to Azure Blob Storage

First, set your Azure Storage connection string as an environment variable:

```
export AZURE_STORAGE_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=bdma;AccountKey=NIQPAT44LNgTWqTBYJII1Q3N5Lecawj60fO0a1RMO+PrD+EPTLj6l6IClThg+UTEbjH1MNIa5vi1+AStTNgA0g==;EndpointSuffix=core.windows.net'
```

Next, create a file named `resources.txt` and list the files you wish to upload to Azure Blob Storage (ABS). Here's an example of the file's contents:

```
amazon_product_links.txt
amazon_products.json
amazon_reviews.json
amazon.log
mediamarkt_products.json
mediamarkt.log
```

Finally, to upload the files to Azure, run:

```
python -m data_collection.azcs_uploader.py
```