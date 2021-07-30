import googlemaps
from datetime import datetime
from typing import Optional, List, Set, Any, Tuple
from dataclasses import dataclass
import logging

LATLON = Tuple[float, float]

@dataclass
class GeoEngine():
    """
    This can wrap any number of external services

    Currently it only implements fetching of elevation using the googlemaps API
    (API KEY required)

    In future this will wrap ORNL Identify
    """
    googlemaps_api_key: str = None
    client = None

    def load_key(self, path: str) -> None:
        with open(path) as stream:
            lines = stream.readlines()
            key = lines[0].strip()
            #print(f'REMOVE THIS: {key}')
            self.googlemaps_api_key = key

    def get_client(self):
        if self.client is None:
            self.client = googlemaps.Client(key=self.googlemaps_api_key)
        return self.client

    def get_elevation(self, latlon: LATLON = (40.714224, -73.961452)):
        results = self.get_client().elevation(latlon)
        return results

    def get_fao_soil_type(self, latlon: LATLON):
        ...

# TODO: Daymet
# curl -L -s 'https://daymet.ornl.gov/single-pixel/api/data?lat=46.372&lon=-119.272&format=json' | jq .
# MODIS:
# curl -L 'https://modis.ornl.gov/rst/api/v1/MCD12Q1/subset?latitude=46.372&longitude=119.272&startDate=A2010001&endDate=A2011001&kmAboveBelow=1&kmLeftRight=1'