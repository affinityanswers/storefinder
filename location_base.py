#!/bin/python
from abc import ABCMeta, abstractmethod
import numpy as np
from numpy import cos, sin, radians, arccos


class NearestLocator:
      """Find the Nearest Loction from the Location Database using the given latitude longitude"""
      __metaclass__ = ABCMeta

      def __init__(self, location_db):
          lat, lng, ids = self.preprocess_location_db(location_db)
          self.lat = lat
          self.lng = lng
          self.ids = ids


      def  preprocess_location_db(self, location_db):
           """ Optimise the Location Database
               location_db: Should be a python list having tuple elements.
                            tuple should be in a order (lat, lng, id)
           """
           lat = np.zeros(len(location_db), dtype=np.float64)
           lng = np.zeros(len(location_db), dtype=np.float64)
           ids = np.zeros(len(location_db), dtype=np.int)
           for i, (lt, ln, id) in enumerate(location_db):
               lat[i] = lt
               lng[i] = ln
               ids[i] = id
           indexes = np.argsort(lat)
           lat = lat[indexes]
           lng = lng[indexes]
           ids = ids[indexes]
           return lat, lng, ids

       
      @abstractmethod
      def process_locations(self, resource_name):
          pass
      

      def find_nearest_locations(self, lat, lng, radius=50):
          km_radius = float(radius) / 1000
          dlat = km_radius / 111.325
          start = np.searchsorted(self.lat, lat - dlat, 'left')
          end = np.searchsorted(self.lat, lat + dlat, 'right')
          qualified_lat = self.lat[start : end]
          qualified_lng = self.lng[start : end]
          qualified_ids = self.ids[start : end]
          distances = 6371 * arccos(cos(radians(lat)) * cos(radians(qualified_lat) ) * cos(radians(qualified_lng ) - radians(lng) ) + sin( radians(lat)) * sin( radians( qualified_lat ) ) )
          distance_qualified = distances <= km_radius
          return set(qualified_ids[distance_qualified])
   
      
