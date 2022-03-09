# Oura CDM

Translate data from an Oura Ring to into a 
[https://ohdsi.github.io/CommonDataModel/](CDM).

# Installation

```bash
git clone https://github.com/jmann277/oura_cdm
cd oura_cdm
pip install -e .
```

The dashboard has extra dependencies:

```bash
pip install altair streamlit
```

The test suite requires pytest:

```bash
pip install altair streamlit
```

One can use pipenv to see the full list of dependencies:

```bash
pip install pipenv
pipenv graph
```

# Environment Variables

For this application to run using real data, you must set your personal
access token as an environment varible:

```bash
export OURA_TOKEN=<token>
```

see [Oura's documentation](https://cloud.ouraring.com/docs/authentication) for
more details

# CLI

To create a folder with the relevant data, execute the following command
from the root of this project:

```bash
python3 oura_cdm/main.py <target_folder_name>
```

# Dashboard

To start the dashboard, execute:

```bash
streamlit run dashboard/main.py
```
