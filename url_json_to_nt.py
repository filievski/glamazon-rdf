import urllib, urllib2, json
from rdflib import Graph
import rdflib
import os, json

def parse_ntriples(name):


    subpath=name[0:3] + "/" 
    newpath="rdf/" + subpath + name.split(".")[0] + ".nt"
    q="https://raw.githubusercontent.com/barnaclebarnes/glamazon/master/organisations/" + subfolder + name
    url = "http://rdf-translator.appspot.com/convert/json-ld/nt/" + q
    try:
        raw_result = urllib2.urlopen(url).read()
    except:
        print "Request error"
        w_err.write(name + "\n")
        return

    g = Graph()
    g.parse(data=raw_result, format="nt")

    g2=Graph()

    for t in g.triples((None, None, None)):
        if type(t[0])==rdflib.term.BNode:
            t0=rdflib.term.URIRef('http://lodlaundromat.org/.well-known/genid/' + t[0])
        else:
            t0=t[0]
        if type(t[2])==rdflib.term.BNode:
            t2=rdflib.term.URIRef('http://lodlaundromat.org/.well-known/genid/' + t[2])
        else:
            t2=t[2]

        g2.add((t0, t[1], t2))

    g2.serialize(destination=newpath, format='ntriples'))


path="/scratch/fii800/glamazon/"

w_err=open("log_errors.txt", "w")

if __name__=="__main__":
    
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".json"):
                parse_ntriples(file)
