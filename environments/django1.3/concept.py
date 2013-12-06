
import sys
from Queue import PriorityQueue
from collections import Counter

from conceptnet.models import Concept
from nltk import pos_tag, word_tokenize

# Please read! To download the resource for tagging 
# import nltk 
# nltk.download('maxent_treebank_pos_tagger')

# Wrapper around default Concept get class for error handling
def getConcept(arg, lang='en'):
  try:
    argConcept = Concept.get(arg,'en')
  except:
    argConcept = None 
  return argConcept

# Take input from user for quick searches
sys.stderr.write("\x1b[2J\x1b[H")
for arg in sys.argv[1:]: 
  argConcept = getConcept(arg,'en')
  print "concept ", arg
  # for ass in argConcept.get_assertions()[:5]: 
  #   print ass 
  # print len(argConcept.get_assertions())

# do BFS 
def doBFS(inpC1str,inpC2str,q): 
  # Convert strings to concepts in ConceptNet 
  inpC1 = getConcept(inpC1str,'en')
  inpC2 = getConcept(inpC2str,'en')
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
    if last_node.text == inpC2.text or last_node.text in inpC2.text or inpC2.text in last_node.text: 
      print "valid path done, found ", tmp 
      print "length of path is ", len(tmp)-1 
      return len(tmp[1:])

    for ast in last_node.get_assertions()[:10]:
      print "assertion is ", ast
      print "corresponding relation name is ", ast.relation.name
      searchC21 = getConcept(ast.concept1.text, 'en')
      searchC22 = getConcept(ast.concept2.text, 'en')
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

# Get common relations that are nouns between strings (unreliable because of conceptnet)
def common_noun_relations(concept_strs): 
  concepts = [getConcept(concept_str,'en') for concept_str in concept_strs]
  concepts = [x for x in concepts if x is not None]
  print concepts 

  set_relations = [set([ast.concept2.text for ast in concept.get_assertions_forward()[:20] \
    if ast.relation.name == "IsA"]) for concept in concepts]
  print set_relations

  all_nouns = []
  for set_relation in set_relations:
    noun_concepts = [] 
    for concept in set_relation: 
      noun_concept = getNoun(concept)
      if noun_concept != []:
        noun_concepts += noun_concept
    all_nouns += [noun_concepts]
  print all_nouns  

# Convert set_relations to a common list in preparation for consensus gathering
def set_to_all_list(set_relations): 
  all_list_relations = []
  for set_relation in set_relations: 
    all_list_relations += list(set_relation) 
  return all_list_relations

# Get common relation words between strings (preffered over common_noun_relations)
# Returns commonality, a measure from 0-1 of what proportion of the tables 
# did the most common attr appear in
def common_relations(concept_strs): 
  concepts = [getConcept(concept_str,'en') for concept_str in concept_strs]
  len_o_concepts = len(concepts) # jaccard over original length of concepts
  concepts = [x for x in concepts if x is not None]

  set_relations = [set([ast.concept2.text for ast in concept.get_assertions_forward()[:20] \
    if ast.relation.name == "IsA"]) for concept in concepts]

  # TODO: make any assertion for amongst cols 

  all_sets = []
  for set_relation in set_relations:
    concepts = [] 
    for concept in set_relation: 
      concepts += concept.split(" ")
    all_sets.append(set(concepts)) 

  # common = set.intersection(*all_sets)
  count_relations = Counter(set_to_all_list(set_relations))

  print count_relations
  commonality = count_relations.most_common(1)[0][1]/float(len_o_concepts)
  print "attr, common values: ", count_relations.most_common(1)[0][0], ", ", commonality

  # If noun concepts worked reliability in NLTK: 
  # noun_concepts = [set([getNoun(concept) for concept in set_relation]) for set_relation in set_relations]
  # print noun_concepts

  return commonality

# Not sure why this is here
def find():
  pass

# Given a string, extracts the nouns from it as list
def getNoun(s): 
  tags = pos_tag(word_tokenize(s))
  tags = [tag[0] for tag in tags if tag[1] == "NN"]
  return tags 

# Get average path length
def getAveragePathLength(lst): 
  return sum(lst)/float(len(list))

# ==============================================================================
# SAMPLE CODE FOR TESTING FUNCTIONS ABOVE 

# testC1 = getConcept('bond', 'en')
# for ass in testC1.get_assertions():
#   print ass
# print len(testC1.get_assertions())
# print "------------------------------"
# testC2 = getConcept('bark', 'en')
# for ass in testC2.get_assertions()[:10]:
#   print ass

# Run BFS 
# inpC1str = 'chair'
# inpC2str = 'stool'

# inpC1str = 'netherlands'
# inpC2str = 'europe'
# print "doing bfs"
# doBFS(inpC1str,inpC2str,[]) 

# Run common_relations 
# concept_strs = ["hyundai", "volvo", "toyota"] # set([u'car'])
# concept_strs = ["dog", "china", "india"] # set([u'animal'])
concept_strs = ["code2", "china", "russia"] # set([u'large', u'country', u'asia'])
common_relations(concept_strs)

# Run getNoun on a string 
# getNoun("animal")

'''
Practical aspects:
TODO: Figure out how to connect and get all this information -- DONE
TODO: Add notion of global score for decision while keeping it general 
  TODO: Add points for schema matching in terms of type 
  TODO: Schema matching (aliases) -- figure out 
  TODO: Add points for homogenity in general, remove for sparsity
  TODO: Presence of foreign key on that dataset that is similar (weigh higher)
  TODO: Amongst cols
TODO: Make the distinction between join and union cases in the final scoring (reuse)'

More theoretical aspects: 
- How to maintain this and keep it updated
- When will this information be added, and how often
'''

