6885_final
==========

Final Project for 6.885 Fall 2013. Intelligent search in DataHub. 

Research Question: Given a table, how can one find best candidates for joins and unions? 

Report Document (in progress): goo.gl/zQW7Zc

To run the code: Go into the /environments/django1.3 folder and run source bin/activate to activate the Django1.3 virtualenv needed to run ConceptNet5.

Major libraries/ technologies used: ConceptNet5, psycopg2

Here is a list of the TODOs for this project.

Practical aspects:
TODO: Figure out how to connect and get all this information -- DONE
TODO: Add notion of global score for decision while keeping it general 
  TODO: Add points for schema matching in terms of type 
  TODO: Schema matching (aliases) -- figure out 
  TODO: Add points for homogenity in general, remove for sparsity
  TODO: Presence of foreign key on that dataset that is similar (weigh higher)
  TODO: Amongst cols do comparison of similarity which leads to 
    TODO: (MAYBE EVENTUALLY) tokenize as english word without punctuations
TODO: Make the distinction between join and union cases in the final scoring (reuse)'

More theoretical aspects: 
- How to maintain this and keep it updated
- When will this information be added, and how often
