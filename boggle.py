
from random import shuffle, sample
from nltk.corpus import wordnet
import math
from btdi import btdi

blocks=[
    "AAEEGN",\
    "ABBJOO",\
    "ACHOPS",\
    "AFFKPS",\
    "AOOTTW",\
    "CIMOTU",\
    "DEILRX",\
    "DELRVY",\
    "DISTTY",\
    "EEGHNW",\
    "EEINSU",\
    "EHRTVW",\
    "EIOSST",\
    "ELRTTY",\
    "HIMNQU",\
    "HLNNRZ"]
    
side = int(math.sqrt(len(blocks)))
width, height = side, side

directions = [[-1, -1], [-1, 0], [-1, 1], \
              [ 0, -1],          [ 0, 1],\
              [ 1, -1], [ 1, 0], [ 1, 1]]
              
found = {}

def isword(w):
    return bool(wordnet.words(w))
    
def shake():
    shuffle(blocks)
    return [ [sample(blocks[row*4 + col],1)[0] for col in range(width)] \
                                              for row in range(height)]

def seek(chain,s=''):
    x,y = chain[-1]
    letter = board[x][y].lower()
    if letter == 'q':
        letter = 'qu'
    s = s + letter
    if (len(s) > 2) and isword(s):
        entry = found.setdefault(s, [])
        if not entry:
            print s # print on first add to list
        entry.append(chain)

    nbor = [[x+d[0],y+d[1]] for d in directions]
    onboard = [d for d in nbor \
               if (d[0] in range(width) and d[1] in range(height))] 
    legal = [l for l in onboard if l not in chain]
    [seek(chain + [l],s) for l in legal]    

def lookup(pointer, stem):
    l,rest=stem[0],stem[1:]
    next = pointer.get(l,None)
    if next is None:
        return None
    if len(stem) == 1:
        if next.get('', None) == {}: # has a sentinel = word
            return 1
        else:
            return 2   # potential word
    return lookup(next,rest)

def seek2(chain,s=''):
    x,y = chain[-1]
    letter = board[x][y].lower()
    if letter == 'q':
        letter = 'qu'
    s = s + letter
    if (len(s) > 2):
        result = lookup(btdi, s)
        if result is None:
            return  # done - no words start like this...
        if result == 1:
            entry = found.setdefault(s, [])
            if not entry:
                print s # print on first add to list
            entry.append(chain)

    nbor = [[x+d[0],y+d[1]] for d in directions]
    onboard = [d for d in nbor \
               if (d[0] in range(width) and d[1] in range(height))] 
    legal = [l for l in onboard if l not in chain]
    [seek2(chain + [l],s) for l in legal]    

                                                
board = shake()                                             
for row in board:
    print ' '.join(row)

for col in range(width):
    for row in range(height):
        seek2([[col,row]])

for k in sorted(found):
    print k
    for v in found[k]:
        print "    ", v

