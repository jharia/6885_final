
import sys
from Queue import PriorityQueue

from conceptnet.models import Concept


# Take input from user for quick searches
sys.stderr.write("\x1b[2J\x1b[H")
for arg in sys.argv[1:]: 
	argConcept = Concept.get(arg,'en')
	print "concept ", arg
	for ass in argConcept.get_assertions(): 
		print ass 
	print len(argConcept.get_assertions())

# Testing
testC1 = Concept.get('bond', 'en')
for ass in testC1.get_assertions():
	print ass
print len(testC1.get_assertions())
print "------------------------------"
testC2 = Concept.get('bark', 'en')
for ass in testC2.get_assertions()[:10]:
	print ass

# do BFS 
def doBFS(inpC1str,inpC2str,q): 
	# Convert strings to concepts in ConceptNet 
	inpC1 = Concept.get(inpC1str,'en')
	inpC2 = Concept.get(inpC2str,'en')
	exp = [inpC1]
	print "added inpc1 to exp"
	q += [exp]
	print "exp enqueued"
	while q!=[]: 
		tmp = q[0]
		q = q[1:]
		last_node = tmp[len(tmp)-1]
		print tmp 
		# print "last node ", last_node
		# print "lasr node text", last_node.text
		# print "inp2 text", inpC2.text
		if last_node.text == inpC2.text or last_node.text in inpC2.text: 
			print "valid path done, found ", tmp 
			print "length of path is ", len(tmp)-1 
			return len(tmp[1:])

		for ast in last_node.get_assertions()[:10]:
			print "assertion is ", ast
			print "corresponding relation name is ", ast.relation.name
			searchC21 = Concept.get(ast.concept1.text, 'en')
			searchC22 = Concept.get(ast.concept2.text, 'en')
			if searchC21.text == last_node.text: 
				searchC2 = searchC22 
			else: 
				searchC2 = searchC21 
			# print "searchc2 is ", searchC2
			if searchC2 not in tmp: 
				# print "searched c2"
				new = []
				new = tmp + [searchC2]
				q += [new]


# Run BFS 
inpC1str = 'chair'
inpC2str = 'stool'

inpC1str = 'honda'
inpC2str = 'car'
print "doing bfs"
doBFS(inpC1str,inpC2str,[]) 

# Get average path length
def getAveragePathLength(lst): 
	return sum(lst)/float(len(list))

# The rest of the project was done using their web api and executing queries 
# such as: 
# http://conceptnet5.media.mit.edu/data/5.1/assoc/list/en/chair,stool
# to find the words associated with both chair and stool, for example.

