# Simple usage
from stanfordcorenlp import StanfordCoreNLP

#nlp = StanfordCoreNLP(r'G:/JavaLibraries/stanford-corenlp-full-2016-10-31/')
#nlp = StanfordCoreNLP(r'/Users/luisvalencia/Projects/Hackaton/CoreNLP/stanford-corenlp-full-2017-06-09/')
nlp = StanfordCoreNLP('http://localhost', port=9001, lang="es")


sentence = 'El perro de San Roque no tiene rabo'
#'Guangdong University of Foreign Studies is located in Guangzhou.'
'''
print ('Tokenize:', nlp.word_tokenize(sentence))
print ('Part of Speech:', nlp.pos_tag(sentence))
print ('Named Entities:', nlp.ner(sentence))
print ('Constituency Parsing:', nlp.parse(sentence))
print ('Dependency Parsing:', nlp.dependency_parse(sentence))
'''
