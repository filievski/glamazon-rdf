import urllib, urllib2, json
from rdflib import Graph
import rdflib
import os, json

def parse_ntriples(name, f):

    content=""
    for line in f:
        content+=line

    #content="@prefix : <http://example.org/#> . :a :b :c ."

    to_check = json.loads(content)
    #print to_check
    try:
        #print to_check["photo"]["license"].lower()
        if to_check["photo"]["license"].lower()=="public domain":
            to_check["photo"]["license"]="https://creativecommons.org/publicdomain/zero/1.0/"
            print "fixed public domain license"
            w.write("fixed public domain license - " + name)
            q={'content': json.dumps(to_check)}
        elif to_check["photo"]["license"]=="CC BY 3.0":
            to_check["photo"]["license"]="https://creativecommons.org/licenses/by-sa/3.0/"
            print "fixed cc by 3.0 license"
            w.write("fixed cc by 3.0 license - " + name)
            q={'content': json.dumps(to_check)}
        elif to_check["photo"]["license"]=="CC BY-SA 3.0":
            to_check["photo"]["license"]="https://creativecommons.org/licenses/by-sa/3.0/"
            print "fixed cc by-sa 3.0 license"
            w.write("fixed cc by-sa 3.0 license - " + name)
            q={'content': json.dumps(to_check)}
        elif to_check["photo"]["license"]=="CC BY-SA 4.0":
            to_check["photo"]["license"]="https://creativecommons.org/licenses/by-sa/4.0/"
            print "fixed cc by-sa 4.0 license"
            w.write("fixed cc by-sa 4.0 license - " + name)
            q={'content': json.dumps(to_check)}
        else:
            q={'content': content}
    except:
        q={'content': content}
    url = "http://rdf-translator.appspot.com/convert/json-ld/nt/content" + "?" + urllib.urlencode(q)
    try:
        raw_result = urllib2.urlopen(url).read()
    #result=json.loads(raw_result)
    except:
        print "Request error"
        w.write("Request error with file " + name)
        return

    g = Graph()
    g.parse(data=raw_result, format="nt")

    g2=Graph()

#    import pprint

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

#    for stmt in g2:
#        pprint.pprint(stmt)

path="/Users/filipilievski/phd/glamazon/"

w=open("log.txt", "w")

if __name__=="__main__":
    
    for subdir, dirs, files in os.walk(path):
        for file in files:
            print file
                #if file!="129910-en.json":
                #continue
            if file.endswith(".json"):
                f=open(os.path.join(subdir, file))
                parse_ntriples(file, f)