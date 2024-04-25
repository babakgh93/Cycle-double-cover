#!/usr/bin/python3 

import random 
import pprint
#import pandas
from sys import argv
import math

class RandomEmbedding:
    """
      My class for computation with random embeddings of a complete graph.
      After initialization in contains a system of (randomly generated) local rotations.
      TODO: Maybe I will actually implement class Embedding, and RandomEmbedding will be a derived class
    """ 
    
    version = 1
    def __init__(self,n):
        self.n = n
        self.rot = []
        self.next = []
        self.seen = set()
        for i in range(n):
            r = [*range(n)]
            r.remove(i)
            random.shuffle(r)

            # next: moving from random list of neighbors to a list representing the cyclic order: next[i][j] is the 
            # neighbor of i that is the next after j (I hope)
            _next = [*range(n)]
            for j in range(n):
                if j != i:
                    _next[j] = r[(r.index(j)+1)%(n-1)]
            self.rot.append(r)
            self.next.append(_next)

    def print(self):
        pprint.pprint(self.rot)
        print()
        print("", [*range(self.n)])
        pprint.pprint(self.next)

    def show_face(self,i,j):
        """
            Walks around a face starting on the edge from i to j (on the right side of it ... we continue accoding to self.next
        """
        last = i; current = j; 
        face = []
        while True: 
            _next = self.next[current][last]
            face.append(_next)
            last, current = current, _next
            self.seen.add((last,current))
            if last == i and current == j:
                break 
        return face

    def compute_face_lengths(self):
        """
            Computes lengths of all faces. 
        """
        self.seen = set()
        self.face_lengths = []
        for i in range(n):
            for j in range(n):
                if i != j and not (i,j) in self.seen:
                    f = self.show_face(i,j)
                    self.face_lengths.append(len(f))

        assert(sum(self.face_lengths) == self.n*(self.n-1))

        self.num_faces = len(self.face_lengths)
        self.avg_face_length = self.n*(self.n-1)/len(self.face_lengths)
        self.root_face_length = len(self.show_face(0,1))


minn = int(argv[1]) 
maxn = int(argv[2]) 
tries = int(argv[3])

fl = [0]*minn
nz = [0]*minn

for n in range(minn,maxn):
    root_face_length = []
    num_zeros = []
    for _ in range(tries):
        x = RandomEmbedding(n).show_face(0,1)
        root_face_length.append(len(x))
        num_zeros.append(x.count(7))

    fl.append(sum(root_face_length)/len(root_face_length))
    print(sorted(root_face_length))
    nz.append(sum(num_zeros)/len(num_zeros))
#    print(n, nz[n]/(n-1))

print()

for n in range(minn,maxn):
    print(n, fl[n]/(n*(n-1)))

print(fl)
print(nz)

#for i in range(3,maxn):
#    print(i, math.log(fl[i])/math.log(i))
