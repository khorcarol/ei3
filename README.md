# SICK 
SICK is package to interface with SICK sensor and automate the data analysis workflow. 
## Installation 
1. Install python3.7.3 (untested)\
`sudo apt install software-properties-common `\
`sudo add-apt-repository ppa:deadsnakes/ppa`\
`sudo apt update`\
`sudo apt install python3.7`
2. Open virtual environment with python3.7. \
`pip3.7 install virtualenv`\
`python3.7 -m virtualenv python3.7env`
`source python3.7env/bin/activate`

2. Dependencies installed as per ```requirements.txt``` 
with \
`pip install -r requirements.txt`
## Usage
 To modify/ add configurations, change the config.json file. 

 To run, use ```python -m main --config config.json ```

To run database unit testing, 
```python -m pytest ``` 

To run visualisation, (UNSTABLE)
```python -m streamlit run web_app/web.py```
Currently only supports running if we are solely recording spectrum and features, (not recording the acceleration data).

## Directories

 #### data 
 This contains data files and a database written to by the sensor. 
 - ```data.db``` is a relational database with two tables, `Raw_data`, which is keyed with `data_id`, and `Inference` which is keyed my `inference_id` 
 - `sx-yyyy-mm-dd_hh-mm-ss.json` data files, where `x` is the `sensor_id` and the rest of the file name is the timestamp at which data is collected. 
 
 #### sick_src 
 This contains the source code for the data acquisition, database handling, feature processing, inferencing, sensor interfacing and visualisation. 
 - `conversion.py` handles conversion from byte encoded data into floats and integers as required 
 -  `data_acquisition.py` acquires data from a sensor and writes data to a local file and database. 
 -   `sensor.py` has all the device specific code such as accessing indices for the spectrum readout. This is where you can choose which sensor data you want (eg raw data from all axis, fft, sensor features)
 
 #### model 
 This is where machine learning models can be added. Currently running one class svm, batch training on all available data and testing on new data point to make inference.
