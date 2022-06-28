
from security_db_base import HashTableBase
import sys


class HashTable(HashTableBase):
    
    primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,
              83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167
              ,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257
              ,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353
              ,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449
              ,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563
              ,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653
              ,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761
              ,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877
              ,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991
              ,997,1009,1013,1019,1021] 
    
    def __init__(self, n_planes, n_passengers):
        for i in range(len(self.primes)):
            if self.primes[i] > n_planes * n_passengers:
                self.size = self.primes[i]
                break
        self.passangers = [None] * self.size 
        self.passanger_count = 0
        self.full_cells = 0
        
    def __len__(self):
        return self.size
        
    @staticmethod
    def hash_codes(key: str):
        n = len(key)
        key = [ord(c) for c in key]
        h1 = 0
        for i in range(n):
            sub =  key[0:i+1]
            h1 = h1 + 1 + sum(sub) 
        return h1 
    
    def add_passenger(self, name, passport_id):
        if self.full_cells == self.size:
            old_size = self.size
            old_passangers = self.passangers
            self.passangers = [None] * (self.max_capacity) 
            self.size = self.max_capacity
            self.passanger_count = 0
            for i in range (old_size):
                if old_passangers[i][0] != "__DEF__":
                    self.add_passenger(old_passangers[i][1], old_passangers[i][0])
                        
        slot = self.get_index(passport_id)
        if  self.passangers[slot] is None:
            self.passangers[slot] = (passport_id, name, 1)
            self.passanger_count = self.passanger_count + 1
            self.full_cells = self.full_cells + 1
        elif self.passangers[slot][2] >= 5:
            sys.stderr.write("Suspicious behaviour")
            return False
        elif self.passangers[slot][1] != name:
            sys.stderr.write("Suspicious behaviour")
            return False
        else:
            num_entries = self.passangers[slot][2] + 1
            self.passangers[slot] = (passport_id, name, num_entries)
        return True
            

    def __delitem__(self, passport_id):
        slot = self.get_index(passport_id)
        if slot != -1 and self.passangers[slot] is not None and self.passangers[slot][0] == passport_id:
            self.passangers[slot] = ("__DEF__", "__DEF__", "__DEF__")
            self.passanger_count = self.passanger_count - 1
            return True
        return False
        
        
    def __getitem__(self, passport_id):
        slot = self.get_index(passport_id)
        if slot != -1 and self.passangers[slot] is not None:
            return self.passangers[slot][1]
        return None
    
    def count(self):
        return self.passanger_count
    
    def get_index(self, passport_id):
        h1 = self.hash_codes(passport_id)
        slot = h1 % self.size
        for i in range(self.size):
            if self.passangers[slot] is None:
                return slot
            elif self.passangers[slot][0] == passport_id:
                return slot     
            slot = (slot + 1) % self.size
        return -1
        
