import csv
import json
#import difflib

from collections import namedtuple

Node = namedtuple("Node", ["id","title","count","duration",
                           "uploaddate","category","upnext","recommends"])
f = open("items_big.csv")
g = open("items_big.json", 'w')
                

reader = csv.reader(f)#, fieldnames = ['id','title','count','duration','uploaddate','category','upnext','recommends'])

data = list(reader)

tree = {id:(title,count,duration,uploaddate,category,upnext,recommends) for
        id,title,count,duration,uploaddate,category,upnext,recommends in data}

nodes = [Node(id,title,count,duration,uploaddate,category,upnext,recommends)
         for id,(title,count,duration,uploaddate,category,upnext,recommends) in tree.items()]

strengths = {}
    
for nodeA in nodes:
    if not nodeA.recommends: continue
    if not nodeA.count: continue
    
    for nodeB in nodes:
        if nodeA.id == nodeB.id:
            continue
        if not nodeB.recommends: continue
        if not nodeB.count: continue
        strength = 0
        if nodeA.category == nodeB.category: strength += .5

        view1, view2 = int(nodeA.count), int(nodeB.count)
        if view1 < view2: view1, view2 = view2, view1
        strength += view2/view1 * .5
#        strength = 1/len(list(difflib.ndiff(nodeA.title, nodeB.title)))

        strengths[(nodeA, nodeB)] = strength

json_data = {}
json_data["nodes"] = [node._asdict() for node in nodes]
json_data["links"] = [{"target":target.id, "source":source.id, "strength":strength} for (target, source), strength in strengths.items()]
json.dump(json_data,g, indent=4)
g.close()
