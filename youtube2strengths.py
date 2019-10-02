import sys
import csv
import json
#import difflib
from collections import namedtuple

Node = namedtuple("Node", ["id","title","count","duration",
                           "uploaddate","category","upnext","recommends"])

def main():
    """Process the csv youtube, and output a json file with link strength
       between all connected videos.
    """
    f = open(sys.argv[1]) # input file
    g = open(sys.argv[2], 'w') # output file
    # Fieldnames for csv file
    # id, title, count, duration, uploaddate, category, upnext, recommends
    reader = csv.reader(f)
    data = list(reader)
    tree = {id:(title,count,duration,uploaddate,category,upnext,tuple(sorted([x.strip().strip("'")for x in recommends.lstrip('[').rstrip(']').split(',')]))) for
            id,title,count,duration,uploaddate,category,upnext,recommends in data}

    nodes = {id:Node(id,title,count,duration,uploaddate,category,upnext,recommends)
             for id,(title,count,duration,uploaddate,category,upnext,recommends) in tree.items()}

    strengths = {}
        
    for nodeA in nodes.values():
        if not nodeA.recommends: continue
        if not nodeA.count: continue

        for nodeB in (nodes[r] for r in nodeA.recommends if r in nodes):
            if nodeA.id == nodeB.id:
                continue
            if not nodeB.recommends: continue
            if not nodeB.count: continue
            strength = 0
##            if nodeA.category == nodeB.category: strength += .5
##
##            view1, view2 = int(nodeA.count), int(nodeB.count)
##            if view1 < view2: view1, view2 = view2, view1
##            strength += view2/view1 * .5
##    #        strength = 1/len(list(difflib.ndiff(nodeA.title, nodeB.title)))
            if nodeA.upnext == nodeB.id or nodeA.id == nodeB.upnext:
                strength = .3
            else:
                strength = .5
            strengths[(nodeA, nodeB)] = strength

    json_data = {}
    json_data["nodes"] = [node._asdict() for node in nodes.values()]
    json_data["links"] = [{"target":target.id, "source":source.id, "strength":strength} for (target, source), strength in strengths.items()]
    json.dump(json_data,g, indent=4)
    g.close()
    f.close()

if __name__ == '__main__':
    main()
