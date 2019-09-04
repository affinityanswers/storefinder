#!/usr/bin/python
from argparse import ArgumentParser
import os
from random import randint
from time import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from location_finder import BenchmarkLocator

def benchmark(test_size, radius):
    global location_finder
    locations_matched  = []
    for i in range(test_size):
        index = randint(0, len(location_finder.lat)) 
        test_lat = location_finder.lat[index]
        test_lng = location_finder.lng[index]
        locations_matched.append(len(location_finder.find_nearest_locations(test_lat, test_lng, radius=radius)))
    return locations_matched

location_finder = None

    
def handle_testing(location_file, test_size, radius, num_process):
    global location_finder
    location_db = []
    with open(location_file, "r") as location_fh:
         for line in location_fh:
             lat, lng, identifier = line.strip().split(",")
             if lat.strip() == "-" or lng.strip() == "-":
                continue
             try:
                location_db.append((float(lat), float(lng), int(identifier)))
             except:
                pass
    location_finder = BenchmarkLocator(location_db)
    with ProcessPoolExecutor(max_workers = num_process) as executor:
         futures = []
         batch_size = test_size // num_process 
         for i in range(num_process):
             if i == num_process - 1:
                process_batch_size = test_size - batch_size * i
             else:
                process_batch_size = batch_size
             print("Job submitted to %d with %d items"%(i, process_batch_size))
             futures.append(executor.submit(benchmark, process_batch_size, radius))
         st = time() * (10 ** 6)
         locations_matched = []
         for future in as_completed(futures):
             locations_matched += future.result()
         et = time() * (10 ** 6)
         print("%d locations in database"%(len(location_finder.lat),))
         print("%.2f locations matched on average"%(sum(locations_matched) / len(locations_matched),))
         print("Time taken for %d locations is %d ms with radius %d meters"%(test_size, (et - st) // 1000, radius))
         print("Average time for one location is %d micro seconds"%((et - st) // test_size,))
         
             
def main():
    parser = ArgumentParser(description="Benchmark the location matching code")
    parser.add_argument("location_db", type=str, help="Points to a csv file which contains list of lat, long, id")
    parser.add_argument("--test_size", type=int, help="Number of locations to test", default=1000)
    parser.add_argument("--radius", type=int, help="radius in meters", default=50)
    parser.add_argument("--num_process", type=int, help="Number of process to use", default=1)
    args = parser.parse_args()
    handle_testing(args.location_db, args.test_size, args.radius, args.num_process)
    


if __name__ == "__main__":
   main()
