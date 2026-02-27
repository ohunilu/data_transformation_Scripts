# CSV to Avro Converter

A simple script to efficiently convert CSV files to Apache Avro format with compression support. This tool is designed to handle large datasets and leverages the reusable data utilities shared with the Parquet converter project.

## Overview

Apache Avro is a row-based data serialization format that offers several advantages:
- **Schema evolution** - supports changing schemas over time
- **Binary format** - compact and efficient encoding
- **Language-independent** - works across multiple programming languages
- **Rich data types** - supports complex nested structures
- **Compression support** - snappy, deflate, bzip2 codecs
- **Compatible** with data processing frameworks like Apache Spark and Hadoop

This project provides a straightforward converter that transforms CSV files into compressed Avro format.

## Features

- ✅ Simple CSV to Avro conversion
- ✅ Configurable compression algorithms (snappy, deflate, bzip2)
- ✅ Reusable utility functions for integration in larger workflows
- ✅ Error handling and validation
- ✅ File size reporting
- ✅ Support for large datasets
- ✅ Shared data utilities with CSV to Parquet converter


### File Descriptions

**avro_converter.py**
- Main entry point for the conversion process
- Demonstrates the typical workflow: read CSV → convert → write Avro
- Uses shared `data_utils.py` from parent directory
- Outputs file with snappy compression

**data_utils.py** (shared)
- Located in parent directory: `../data_utils.py`
- `read_csv_file()` - Reads CSV files with error handling and reporting
- `write_avro_file()` - Writes Avro files with configurable compression
- Designed for reuse across multiple conversion projects


## Installation

### 1. Navigate to the project directory

```bash
cd /path/to/Convert_csv_to_avro
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start - Run the Converter

```bash
python avro_converter.py
```

This will convert `sample_data.csv` to `sample_data.snappy.avro` in the current directory.


## Resources

- [Apache Avro Documentation](https://avro.apache.org/)
- [Apache Avro Python](https://avro.apache.org/docs/current/python/)
- [PyArrow Avro Support](https://arrow.apache.org/docs/python/parquet.html)
- [Avro vs Parquet Comparison](https://www.upsolver.com/blog/apache-avro-parquet-orc-file-formats)
