import requests
import json
from typing import Dict, Any, Tuple
from conversion import bytes_to_float32


class Sensor:
    """
    A class for interacting with sensor.
    """

    def __init__(self, ip_address="10.0.0.166", indices={"kurtosis_X": (4495, 1),
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

    def post_http(self, index: int, payload, subindex=None):
        if subindex is not None:
            url = "http://" + self.ip_address + "/iolink/v1/devices/master1port1/parameters/" + \
                str(index) + "/subindices/" + str(subindex) + "/value"
        else:
            url = "http://" + self.ip_address + "/iolink/v1/devices/master1port1/parameters/" + \
                str(index) + "/value"
        response = requests.post(url, data=json.dumps(payload))

    def get_http(self, index, subindex=None):
        if subindex is not None:
            url = "http://" + self.ip_address + "/iolink/v1/devices/master1port1/parameters/" + \
                str(index) + "/subindices/" + str(subindex) + "/value"
        else:
            url = "http://" + self.ip_address + "/iolink/v1/devices/master1port1/parameters/" + \
                str(index) + '/value'
        r = requests.get(url)
        data = r.json()
        return data["value"]

    def get_sensor_data(self):
        res = {}
        res.update(self.get_sensor_fft())
        res.update(self.get_sensor_features())
        return res

    def get_sensor_fft(self):
        self.post_http(4585, payload={"value": [2]})
        v = [0]
        while v != [2]:
            v = self.get_http(4586, 1)

        self.post_http(4589, payload={"value": [0]}, subindex=1)

        spectrum = []
        for i in range(37):
            data = self.get_http(4590)
            for i in range(0, len(data), 4):
                res = bytes_to_float32(data[i:i+4])
                spectrum.append(res)

        self.post_http(4585, payload={"value": [0]})

        return {"spectrum": spectrum}

    def get_sensor_raw():
        return

    def get_sensor_features(self):
        res = {}
        for key, (index, subindex) in self.indices.items():
            res[key] = bytes_to_float32(
                self.get_http(index, subindex=subindex))
        return res
