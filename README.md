# SICK 
SICK is package to interface with SICK sensor and automate the data analysis workflow. 
## Installation 
1. RevPi with python3.7 opened as a virtual environment. 
2. Dependencies installed as per ```requirements.txt``` 
## Usage
 To modify/ add configurations, change the config.json file. 
 ```bash python -m main --config config.json ```

To run database unit testing, 
```bash python -m pytest ``` 

## Directories

 #### data 
 This contains data files and a database written to by the sensor. 
 - ```data.db``` is a relational database with two tables, `Raw_data`, which is keyed with `data_id`, and `Inference` which is keyed my `inference_id` 
 - `sx-yyyy-mm-dd_hh-mm-ss.json` data files, where `x` is the `sensor_id` and the rest of the file name is the timestamp at which data is collected. 
 
 #### sick_src 
 This contains the source code for the data acquisition, database handling, feature processing, inferencing, sensor interfacing and visualisation. 
 - `conversion.py` handles conversion from byte encoded data into floats and integers as required 
 -  `data_acquisition.py` acquires data from a sensor and writes data to a local file and database. 
 -   `sensor.py` has all the device specific code such as accessing indices for the spectrum readout 
 
 #### model 
 This is where machine learning models can be added. Currently running one class svm, batch training on all available data and testing on new data point to make inference.