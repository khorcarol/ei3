import time
import requests
import json
from typing import Dict, Any, Tuple, List, Union
from sick_src.conversion import bytes_to_float32, bytes_to_int16, bytes_to_int16_be


class Sensor:
    """
    A class for interacting with sensor.
    """
    def __init__(self, sensor_id, port, ip_address="cogsihq.dyndns.org:8000", indices={"kurtosis_X": (4495, 1),
                                                         "kurtosis_Y": (4495, 2),
                                                         "kurtosis_Z": (4495, 3),

                                                         "td_aRMS_X": (4483, 1),
                                                         "td_aRMS_Y": (4483, 2),
                                                         "td_aRMS_Z": (4483, 3),
                                                         "td_aRMS_mag": (4483, 4),

                                                         "td_vRMS_X": (4486, 1),
                                                         "td_vRMS_Y": (4486, 2),
                                                         "td_vRMS_Z": (4486, 3),
                                                         "td_vRMS_mag": (4486, 4),

                                                         "skewness_X": (4492, 1),
                                                         "skewness_Y": (4492, 2),
                                                         "skewness_Z": (4492, 3),

                                                         "variance_X": (4489, 1),
                                                         "variance_Y": (4489, 2),
                                                         "variance_Z": (4489, 3),

                                                         "shape_X": (4502, 1),
                                                         "shape_Y": (4502, 2),
                                                         "shape_Z": (4502, 3),

                                                         "crest_X": (4504, 1),
                                                         "crest_Y": (4504, 2),
                                                         "crest_Z": (4504, 3),

                                                         "impact_X": (4507, 1),
                                                         "impact_Y": (4507, 2),
                                                         "impact_Z": (4507, 3),

                                                         "peaktopeak_X": (4489, 1),
                                                         "peaktopeak_Y": (4489, 2),
                                                         "peaktopeak_Z": (4489, 3),

                                                         }):
        self.ip_address = ip_address
        self.indices = indices
        self.sensor_id = sensor_id
        self.port = port

    def post_http(self, index: int, payload, subindex=None):
        while True:
            try:

                if subindex is not None:
                    url = "http://" + self.ip_address + "/iolink/v1/devices/master1port" + self.port + "/parameters/" + \
                        str(index) + "/subindices/" + str(subindex) + "/value"
                else:
                    url = "http://" + self.ip_address + "/iolink/v1/devices/master1port" + self.port + "/parameters/" + \
                        str(index) + "/value"
                response = requests.post(url, data=json.dumps(payload))
                print(url)
                return
            except:
                print("Retrying")
                time.sleep(0.1)

    def get_http(self, index, subindex=None):
        while True:
            try:
                if subindex is not None:
                    url = "http://" + self.ip_address + "/iolink/v1/devices/master1port" + self.port + "/parameters/" + \
                        str(index) + "/subindices/" + str(subindex) + "/value"
                else:
                    url = "http://" + self.ip_address + "/iolink/v1/devices/master1port" + self.port + "/parameters/" + \
                        str(index) + '/value'
                
                r = requests.get(url)
                print(url)
                data = r.json()
                return data["value"]
            except:
                print("Retrying")
                time.sleep(0.1)

    def get_sensor_data(self) -> Dict[str, Union[List[int], int]]:
        '''
        Returns dictionary mapping item name to item value
        e.g. key "spectrum" to list of values of FFT spectrum
        e.g. key "freq_incr" to frequency increment int value
        '''

        res = {}
        res.update(self.get_sensor_fft())
        # res.update(self.get_raw_data_all_axis())
        res.update(self.get_sensor_features())
        return res

    def get_sensor_fft(self) -> Dict[str, List[int]]:
        self.post_http(4585, payload={"value": [2]})
        v = [0]
        while v != [2]:
            v = self.get_http(4586, 1)

        self.post_http(4589, payload={"value": [0]}, subindex=1)
        nr_of_segments = self.get_http(4586, 3)[0]
        nr_of_valid_points = bytes_to_int16(self.get_http(4586, 2))
        freq_incr = bytes_to_float32(self.get_http(4586, 5))

        spectrum = []
        for i in range(nr_of_segments):
            data = self.get_http(4590)
            for i in range(0, len(data), 4):
                res = bytes_to_float32(data[i:i+4])
                spectrum.append(res)
        spectrum = spectrum[:nr_of_valid_points]

        self.post_http(4585, payload={"value": [0]})
        return {"spectrum": spectrum, "freq_incr": freq_incr}

    def get_raw_data_by_axis(self,axis: int):
        self.post_http(4585, payload={"value": [1]})
        v = [0]
        while v != [1]:
            v = self.get_http(4586, 1)
        self.post_http(4587, payload={"value": [axis]}, subindex=2)
        self.post_http(4587, payload={"value": [0]}, subindex=1)

        raw_data_nr_segments = self.get_http(4586, subindex=3)[0]
        nr_points = bytes_to_int16(self.get_http(4586, subindex=2))

        spectrum = []
        for n in range(raw_data_nr_segments):
            data = self.get_http(4588)
            for i in range(0, len(data), 2):

                spectrum.append(bytes_to_int16_be(data[i:i+2]) * 244/1e6)
        self.post_http(4585, payload={"value": [0]})

        return spectrum[:nr_points]


    def get_raw_data_all_axis(self,):
        return {
            "acc_X": self.get_raw_data_by_axis(axis=1),
            "acc_Y": self.get_raw_data_by_axis(axis=2),
            "acc_Z": self.get_raw_data_by_axis(axis=3)

        }


    def get_sensor_features(self) -> Dict[str, int]:
        res = {}
        for key, (index, subindex) in self.indices.items():
            res[key] = bytes_to_float32(
                self.get_http(index, subindex=subindex))
        return res



