# WEBTEXTEN - Web Text Extraction Node

WEBTEXTEN is a versatile web text extraction application designed to crawl websites, extract textual content from web pages and PDFs, and save the extracted content into organized text files. This tool is ideal for web scraping tasks where large volumes of web data need to be processed and stored efficiently.

Key Features
- Web Crawling: Traverses web pages starting from a given URL, following links within the same domain to gather content comprehensively.
- Content Extraction: Extracts text from HTML elements such as paragraphs and headers, as well as from PDF files.
- File Conversion and Saving: Converts extracted content into text files, ensuring it is stored in a structured and accessible format.
- URL Filtering and Throttling: Implements rules to skip irrelevant URLs and throttles requests to avoid overloading web servers.
- Logging and Reporting: Maintains detailed logs of the crawling and extraction process, including any errors encountered.

## Git Repositories
- https://github.com/msuliot/texten.git
- https://github.com/msuliot/webtexten.git
- https://github.com/msuliot/chunken.git
- https://github.com/msuliot/datamyn.git

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed Python 3.7 or later.
- You have a working internet connection.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/msuliot/webtexten.git
    cd texten
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the WEBTEXTEN application, use the following command:

```bash
python app.py
```

### Configuration

The configuration is managed through a `config.json` file. Create a configuration file with the following structure:

```json
{
  "text_output_directory": "path/to/text/output/directory",
  "pii_output_directory": "path/to/pii/output/directory",
  "hash_file_path": "file_hashes.json",
  "scheduler_interval": 60
}
```