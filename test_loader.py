from collections import deque
import os
from os.path import join, isfile
import re

def list_directories(path):
    # 
    return [f for f in os.listdir(path) if not isfile(f)]

class test_loader:
    def __init__(self, root_path):
        self.root_path = root_path
    
    def load_types(self):
        dirs = list_directories(self.root_path)
        matched = [d for d in dirs if re.search(r"[0-9][0-9][A-Za-z]+$", str(d))]
        self.types = sorted(matched)
        return self.types

    def set_types(self, type_index):
        assert(type_index < len(self.types))
        assert(type_index >= 0)

        self.type = self.types[type_index]
    
    def get_type(self):
        return self.type
    
    def load_sizes(self):
        assert(self.type)
        dirs = list_directories(join(self.root_path,self.type))
        matched = [d for d in dirs if re.search(r"n[0-9]+$", str(d))]
        self.sizes = sorted(matched)
        return self.sizes
    
    def set_sizes(self, size_index):
        assert(size_index < len(self.sizes))
        assert(size_index >= 0)
        self.size = self.sizes[size_index]
    
    def get_size(self):
        return self.size
    
    def load_ranges(self):
        assert(self.size)

        dirs = list_directories(join(self.root_path,self.type,self.size))
        matched = [d for d in dirs if re.search(r"R[0-9]+$", str(d))]
        self.ranges = sorted(matched)
        return self.ranges
    
    def set_range(self, range_index):
        assert(range_index < len(self.ranges))
        assert(range_index >= 0)
        self.range = self.ranges[range_index]
    
    def get_range(self):
        return self.range
    
    def load_tests(self):
        assert(self.range)

        dirs = list_directories(join(self.root_path,self.type,self.size, self.range))
        matched = [d for d in dirs if re.search(r"s[0-9]+\.kp$", str(d))]
        self.tests = sorted(matched)
        return self.tests

    def set_test(self,test_index):
        assert(test_index < len(self.tests))
        assert(test_index >= 0)
        self.test = self.tests[test_index]

    def read_raw(self):
        path = join(self.root_path,self.type,self.size, self.range, self.test)

        raw = deque([])
        with open(path, 'r') as f:
            for line in f:
                for s in line.split():
                    raw.append(int(s))
        return raw
    
    def parse_test(self):
        raw = self.read_raw()

        no_items = raw.popleft()
        capacities = [raw.popleft()]

        values = []

        weights = []

        for i in range(no_items):
            values.append(raw.popleft())
            weights.append(raw.popleft())
    
        return no_items, capacities, values, [weights]

 




def test(path):
    loader = test_loader(path)
    test_types = loader.load_types()
    loader.set_types(1)

    test_sizes = loader.load_sizes()
    loader.set_sizes(1)

    test_ranges = loader.load_ranges()
    print(test_ranges)
    loader.set_range(1)

    tests = loader.load_tests()
    loader.set_test(11)

    print(loader.parse_test())
