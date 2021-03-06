import solr
import json

def make_ner_dict(data):
	return dict([(x["id"],[x["measurments"],x["location"]]) for x in data])
	
def get_ner_nodes(querystring,fileid):
	if fileid in nerdata:
		children = [{"name":c,"parent":fileid} for c in nerdata[fileid]]
		return {"name":fileid,"parent":querystring,"children":children}

def get_requestresponsetree(querystring):
	res = s.query(querystring,rows=500)
	ids = [x["id"] for x in res.results]
	print querystring,len(ids)
	filenodes = filter(lambda x:x,map(lambda fileid:get_ner_nodes(querystring,fileid),ids))
	with open(querystring.replace(" ","_")+"_tree.json","w") as f:
		json.dump([{"name":querystring,"parent":"null","children":filenodes}],f)

if __name__ == "__main__":
	with open("ner2.json") as f:
		nerdata = json.load(f)
	print len(nerdata)
	nerdata = make_ner_dict(nerdata)

	s = solr.SolrConnection('http://localhost:8983/solr/polarcollectionNew')

	querystrings = ["polar bear","global warming","arctic ice"]
	map(get_requestresponsetree,querystrings)
