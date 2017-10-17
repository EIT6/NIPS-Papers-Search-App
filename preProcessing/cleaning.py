from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
import sys
import pandas as pd
import isAscii
csv.field_size_limit(sys.maxsize)
def removeStopWords():
	rows = []
	with open('papers.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter = ' ', quotechar='|')
		for row in reader:
			#print ' '.join(row)
			rows.append(row)
	stopWords = set(stopwords.words('english'))
	with open ('editedCsv.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter = ' ', quotechar='|', quoting = csv.QUOTE_MINIMAL)
		for row in rows:
			filteredRow = []
			for word in row:
				if word.lower() not in stopWords:
					filteredRow.append(word)
			writer.writerow(filteredRow)

def createDroppedDocumentsList(dropped_documents):
	df = pd.DataFrame(dropped_documents)
	df.to_csv("dropped_documents.csv", sep = ',')


def removeIncorrectEntries():
	document = pd.read_csv("editedCsv.csv")
	paper_texts = document.paper_text
	dropped_documents = []
	for i in range(len(paper_texts)): #still doesn't work
		if isAscii.isValidPaper(paper_texts[i]) == False:
			print "Dropped:%s" % document.title[i]
			dropped_documents.append(document.paper_text[i])
			#document.drop(i, inplace = True)
	createDroppedDocumentsList(dropped_documents)

if __name__ == '__main__':
	removeIncorrectEntries()

	#removeStopWords()
		
