# IKMC Dashboard

## Overview

The IKMC Dashboard is a Streamlit application used for monitoring, analyzing, and visualizing key indicators for the IKMC program.

## Features

- Interactive KPI dashboard
- Cohort monitoring
- Outborn analytics
- Discharge analytics
- Excel data export
- Live dashboard refresh
- REST API integration

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- Requests
- python-dotenv

## Project Structure

```
components/
pages/
services/
app.py
requirements.txt
```

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```env
IKMC_API_KEY=YOUR_API_KEY_HERE
```

## Running the Dashboard

```bash
streamlit run app.py
```

## Notes

- API credentials are loaded from environment variables using `python-dotenv`.
- Local testing and debugging scripts are excluded from version control.
- This project is intended for internal use.