import sys

sys.path.append(r'F:\dev\python')

import query
reload(query)
from query import *
import timeit
import types


index = None
bindex = None

def build1():
    global index
    index = buildindex(layer, 'postcode')
    
def build2():
    global bindex
    bindex = buildBIndex(layer, 'postcode')
    
qstring = "postcode = 6164"
qstring2 = "subdivided = 'Y'"
top = 5
   
def withindex():
    layer = iface.activeLayer()
    q = query(layer).where(qstring).top(top).with_index(index)
    results = q().next()
        
def withbindex():
    layer = iface.activeLayer()
    q = query(layer).where(qstring).top(top).with_index(bindex)
    results = q().next()
    
def without():   
    layer = iface.activeLayer()
    q = (query(layer).where(qstring)
                    .where(qstring2)
                    .top(top))
    results = q()
    out = results.next()
    
def without_select():   
    layer = iface.activeLayer()
    q = (query(layer).where(qstring)
                    .where(qstring2)
                    .top(top))
    results = q()
    out = results.next()
    assert isinstance(out, dict)
    print out
        
def with_select():
    def checkassessment(feature):
        if feature['assessment'] is None:
            return False
            
        return int(feature['assessment']) == 4315968
        
    layer = iface.activeLayer()
    q = (query(layer).where("postcode = 6164")
                    .where("subdivided = 'Y'")
                    .where(checkassessment)
                    .top(top)
                    .select('assessment', 
                            'address', 
                            'lot',
                            geom = lambda f: f.geometry(),
                            mylot = lambda f: int(f['house_numb']) * 100))
    results = q()
    out = results.next()
    assert isinstance(out, dict)
    print out
    
def with_select_customfunction():
    def MyValue(feature):
        return "Hello World"
        
    layer = iface.activeLayer()
    q = (query(layer).top(1)
                    .select(MyValue))

    results = q()
    out = results.next()
    print out
    assert isinstance(out, dict)
    assert "MyValue" in out.keys()
        
def with_select_mapview():
    layer = iface.activeLayer()
    q = (query(layer).restict_to(Query.MapView())
                    .top(top)
                    .select('assessment', 
                            'address', 
                            'lot',
                            geom = lambda f: f.geometry(),
                            mylot = lambda f: int(f['house_numb']) * 100)
        )

    results = q()
    out = results.next()
    assert isinstance(out, dict)
    print out

print 
print "No Index:"
functions = [without, 
            with_select, 
            with_select_mapview, 
            without_select,
            with_select_customfunction]
timings = {}
for func in functions:
    print func.__name__
    timings[func.__name__] = timeit.timeit(func, number=1), '(1 run)'
    
for name, time in timings.items():
    print name, time

