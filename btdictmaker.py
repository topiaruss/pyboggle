# quick utility to build python source for an incrementally searched
# dictionary tree.
# Russ Ferriday, russf@topia.com - Sept 2010
# 
from nltk.corpus import wordnet
ss=wordnet.all_synsets()

root={}
count = 0
for s in ss:
    s=s.name.split('.')[0]
    if len(s) > 16 or len(s) < 3: 
        continue  # we can only use letters once - only interested > 2
    if '_' in s:
        continue  #ignore terms
    cursor=root
    for i in range(len(s)):
        l=s[i]
        cursor=cursor.setdefault(l,{})
        if i == len(s)-1:
            cursor['']={}  # put a sentinel to mark word end
    count += 1
print 'dict setup complete'

#Testing....

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
        
print lookup(root, 'ascetic')
print lookup(root, 'abs')
print lookup(root, 'xx')
print count

if 1:
    import pprint
    f=file('btdi.py','w')
    f.write("btdi=")
    pp = pprint.PrettyPrinter(indent=1,stream=f)
    pp.pprint(root)
    f.close()
    print 'done pprint'

#pickles are bigger than text, and text compiles pretty fast so forget this...
#import cPickle
#f=file('btdi.pickle','w')
#cPickle.dump(root,f)
#f.close()