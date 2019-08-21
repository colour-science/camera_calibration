import numpy as np
import json
from collections import namedtuple


class Camera(object):
    Device = namedtuple("Device", ["manufacturer", "name"])
    Image = namedtuple("Image", ["shape", "raw_extension", "bias", "bayer_pattern", "bit_depth"])
    Settings = namedtuple("Settings", ["ISO_min", "ISO_max", "exposure_min", "exposure_max"])

    def __init__(self, device_properties, image_properties, settings):
        self.device = self.Device(**device_properties)
        self.image = self.Image(**image_properties)
        self.settings = self.Settings(**settings)

        self.bayer_map = self.generate_bayer_map()

    def __repr__(self):
        device_name = f"{self.device.manufacturer} {self.device.name}"
        return device_name

    def _as_dict(self):
        dictionary = {"device": self.device._asdict(),
                      "image": self.image._asdict(),
                      "settings": self.settings._asdict()}
        return dictionary

    def generate_bayer_map(self):
        bayer_map = np.zeros(self.image.shape, dtype=int)
        bayer_map[0::2, 0::2] = self.image.bayer_pattern[0][0]
        bayer_map[0::2, 1::2] = self.image.bayer_pattern[0][1]
        bayer_map[1::2, 0::2] = self.image.bayer_pattern[1][0]
        bayer_map[1::2, 1::2] = self.image.bayer_pattern[1][1]
        return bayer_map

    def write_to_file(self, path):
        write_json(self._as_dict(), path)

    @classmethod
    def read_from_file(cls, path):
        full_dictionary = load_json(path)
        device_properties, image_properties, settings = full_dictionary.values()
        return cls(device_properties, image_properties, settings)


def load_json(path):
    """
    Read a JSON file.
    """
    file = open(path)
    dump = json.load(file)
    return dump


def write_json(data, save_to):
    """
    Write a JSON file containing `data` to a path `save_to`.
    """
    with open(save_to, "w") as file:
        json.dump(data, file)


def load_metadata(root):
    """
    Read the metadata JSON located in the `root` folder.
    """
    metadata = load_json(root/"info.json")
    return metadata
