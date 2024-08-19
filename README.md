# SICK 
SICK is package to interface with SICK sensor and automate the data analysis workflow. 
## Installation 
1. Reformat Pi by downloading new image onto Pi, which should include python3.11.
- Download Raspberry Pi Imager
- Use Raspberry Pi model 5, 32 bit
- Allow SSH
- Find out its IP by running IP search on local Wifi

2. Open virtual environment with python3.11 (should be default on the Pi) \
`python3 -m venv python3.11`\
`source python3.11/bin/activate`

3. Get source code with
`git clone https://khorcarol@github.com/khorcarol/ei3.git`

4. Run `sudo apt-get install libopenblas-dev`


3. Dependencies installed with \
`pip install -r requirements.txt`

## Usage
 To modify/ add configurations, change the config.json file. 

 To run, use ```python -m main --config config.json ```

To run database unit testing, 
```python -m pytest ``` 

To run visualisation, (UNSTABLE)
```python -m streamlit run web_app/web.py```
Currently only supports running only on laptop, if we are solely recording spectrum and features, (not recording the acceleration data).

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
