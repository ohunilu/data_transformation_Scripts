# CSV to Parquet Converter

 Here is a small script to efficiently convert CSV files to Apache Parquet format with compression support. This tool is designed to handle large datasets and includes reusable utilities for data transformation workflows. The sample data used to demonstrate the conversion reduced the file size by 74%! I have included at the end of this README  resources I explored so you can improve it to fit your need.

## Overview

Parquet is a columnar storage format that offers significant advantages over CSV:
- **Reduced file size** through compression (snappy, gzip, brotli, etc.)
- **Faster read/write operations** due to columnar organization
- **Better performance** when querying specific columns
- **Type preservation** maintains data types during serialization
- **Compatible** with data processing frameworks like Apache Spark, Pandas, and DuckDB

This script provides a straightforward converter that transforms CSV files into compressed Parquet format, along with reusable utility functions for batch processing workflows.

## Features

- ✅ Simple CSV to Parquet conversion
- ✅ Configurable compression algorithms (snappy)
- ✅ Flexible engine selection (auto: pyarrow | fastparquet)
- ✅ Reusable utility functions for integration in larger workflows
- ✅ Error handling and validation
- ✅ File size reporting
- ✅ Support for large datasets
- ✅ Column and row counting


### File Descriptions

**parquet_converter.py**
- Main entry point for the conversion process
- Demonstrates the typical workflow: read CSV → convert → write Parquet
- Uses the IKEA product catalog as an example dataset
- Outputs file with snappy compression

**data_utils.py**
- `read_csv_file()` - Reads CSV files with error handling and reporting
- `write_parquet_file()` - Writes Parquet files with configurable compression
- Designed for reuse in other projects and automation scripts


## Installation

### 1. After Cloning the project, navigate into the covert folder

```bash
cd /path/to/Convert_csv_to_parquet
```

### 2. Create a python environment

```bash
python3 -m venv venv
```

### 3. Install dependencies into the venv environment

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Navigate to the root project directory of the repo

```bash
cd /path/to
```

### 5. Run the convert script from the root project directory

```bash
python3 -m converters.convert_csv_to_parquet.parquet_converter
```

This will convert `IKEA_product_catalog.csv` to `IKEA_convert.snappy.parquet` in the current directory.


## Resources

- [Apache Parquet Documentation](https://parquet.apache.org/)
- [Pandas to_parquet() Reference](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html)
- [PyArrow Documentation](https://arrow.apache.org/docs/python/)
- [Parquet vs CSV Performance](https://towardsdatascience.com/parquet-vs-csv-f5e2fbb5c44e)test
