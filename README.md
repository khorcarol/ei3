# SICK

SICK is package to interface with SICK sensor and automate the data analysis workflow.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SICK.

```bash
pip install foobar
```

## Usage

```bash
python -m main --config config.json
```
To modify/ add configurations, change the config.json file.

```bash
python -m pytest 
```
```bash
streamlit run web_app/web.py
```
## Directories
#### data
This contains data files and a database written to by the sensor.

#### sick_src
This contains the source code for the data acquisition, database handling, feature processing, inferencing, sensor interfacing and visualisation.

#### model
This is where machine learning models can be added.