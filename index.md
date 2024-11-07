# Data Wrangling and Engagement Insights

**Author**: Sally Marcellina Yeo  

## Overview

This repository contains my submission for the End-of-Course Assignment (ECA) for the ANL503 Data Wrangling course. The project focuses on generating insights from auto-generated Zoom class transcripts. The tasks include data extraction, data transformation, and visualization to analyze student engagement based on participation captured through dialogue in a `.vtt` file.

## Key Components

### 1. Data Extraction and Transformation
- **Python Script**: A Python program is used to read a `.vtt` (Web Video Text Tracks) file, parse it, and extract dialogue components (SNo, TimeFrom, TimeTo, RegName, and Utterance).
- **MySQL Database**: The extracted data is stored in a MySQL table called `vtt`. A new table `vttclean` is created with an additional column that calculates the dialogue duration in milliseconds.

### 2. Visualization
- **R Script**: An R script generates a barchart showing the total airtime (in milliseconds) for each student who participated in the Zoom session.

## Project Structure

- **`503eca_1a.py`**: Python script for extracting dialogue components from the `.vtt` file and storing the data in a MySQL table.
- **`503eca_1b.sql`**: SQL script that creates a new table with dialogue duration in milliseconds and performs data transformations.
- **`503eca_1c.R`**: R script that reads data from MySQL, filters it, and generates a barchart showing student participation airtime.

# Python Script Explanation

Import necessary library:

```python
import os   # to set working directory
import re   # for regex
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
```
Defining Regex:

```python
# Define regex for parsing
INIT_regex = re.compile(r'^WEBVTT\s*$')
SNo_regex = re.compile(r'^(\d+)\s*$')
Time_regex = re.compile(r'^(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\s*$')
NameUtt_regex = re.compile(r'^([^:]+):\s?(.*)$')
```
