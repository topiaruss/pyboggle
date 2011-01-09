# boggle
# Russ Ferriday, russf@topia.com
# September 2010
# 
from random import shuffle, sample
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
    
def shake():
    shuffle(blocks)
    return [ [sample(blocks[row*4 + col],1)[0] for col in range(width)] \
                                              for row in range(height)]

def lookup(pointer, stem):
    l,rest=stem[0],stem[1:]
    next = pointer.get(l,None)
    if next is None:
        return None
    if len(stem) == 1:               #final letter in input
        if next.get('', None) == {}: # has a sentinel -- it's a word
            return 1
        else:
            return 2   # potential word
    return lookup(next,rest)

def seek(chain,s=''):
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
                pass
                #print s # print on first add to list
            entry.append(chain)

    nbor = [[x+d[0],y+d[1]] for d in directions]
    onboard = [d for d in nbor \
               if (d[0] in range(width) and d[1] in range(height))] 
    legal = [l for l in onboard if l not in chain]
    [seek(chain + [l],s) for l in legal]    

                                                
board = shake()               
                  
#print the board            
for row in board:
    print ' '.join(row)

#start with each letter in order
for col in range(width):
    for row in range(height):
        seek([[col,row]])

print
print "ok, well, I'm finished ;)"
print """
Although I do boast a bit, I'm still not smart enough to know whether a word 
in my dictionary is a name, like AMUR, which is an Asian river. So 
I would count that as a word, when I really should not. :(
"""
if 'Q' in [item for sublist in board for item in sublist]:
    print""" Oh, and remember that Q means "Qu", and counts as 2 letters.\n"""
raw_input("hit <return> when you are ready for me to reveal my %s words!" % len(found) ) 
print 'collated and sorted word with their traversal chains'
for k in sorted(found):
    print k
    for v in found[k]:
        print "    ", v

