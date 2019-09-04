import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from location_base import NearestLocator

class BenchmarkLocator(NearestLocator):
      def process_locations(self, resource_name):
          pass


