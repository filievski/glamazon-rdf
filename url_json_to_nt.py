import urllib, urllib2, json
from rdflib import Graph
import rdflib
import os, json

def parse_ntriples(name, f):


    subpath=name[0:3] + "/" 
    newpath="rdf/" + subpath + name.split(".")[0] + ".nt"
    q="https://raw.githubusercontent.com/barnaclebarnes/glamazon/master/organisations/" + subpath + name
    url = "http://rdf-translator.appspot.com/convert/json-ld/nt/" + q
    try:
    	raw_result = urllib2.urlopen(url).read()
    except:
        print "Request error. Trying to query with the full json"

	content=""
	for line in f:
            content+=line

    #content="@prefix : <http://example.org/#> . :a :b :c ."

    	try:
    	    to_check = json.loads(content)
	    q={'content': content}
    	    url = "http://rdf-translator.appspot.com/convert/json-ld/nt/content?" + urllib.urlencode(q)
            raw_result = urllib2.urlopen(url).read()
    	#result=json.loads(raw_result)
    	except:
            print "Request error both ways"
            w_err.write(name + "\n")
            return

    g = Graph()
    g.parse(data=raw_result, format="nt")

    g2=Graph()
    main_entity=None
    for t in g.triples((None, rdflib.term.URIRef('http://schema.org/mainEntityOfPage'), None)):
	main_entity=t[0]


    main_uri = rdflib.term.URIRef('http://www.museums.io/museums/' + name.split('.')[0])
    for t in g.triples((None, None, None)):
        if type(t[0])==rdflib.term.BNode:
	    if t[0]==main_entity:
		t0=main_uri
	    else:
                t0=rdflib.term.URIRef('http://lodlaundromat.org/.well-known/genid/' + t[0])
        else:
            t0=t[0]
        if type(t[2])==rdflib.term.BNode:
            t2=rdflib.term.URIRef('http://lodlaundromat.org/.well-known/genid/' + t[2])
        else:
            t2=t[2]

        g2.add((t0, t[1], t2))

    g2.add((main_uri, rdflib.term.URIRef('http://rdfs.org/ns/void#inDataset'), rdflib.term.URIRef('http://www.museums.io/museums/void.nt#Glamazon')))

    g2.serialize(destination=newpath, format='nt')


path="/scratch/fii800/glamazon/"

w_err=open("new_errors.txt", "w")
r_err=open("log_errors.txt", "r")

if __name__=="__main__":
 
    for file in r_err:
	file=file.strip()
	if file!="":
	    f=open("/scratch/fii800/glamazon/organisations/" + file[0:3] + "/" + file, "r")
	    parse_ntriples(file, f)
#    for subdir, dirs, files in os.walk(path):
#        for file in files:
#            if file.endswith(".json"):
#                f=open(os.path.join(subdir, file))
#		parse_ntriples(file, f)
