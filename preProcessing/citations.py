from __future__ import division
import pandas as pd
import isAscii
import json
import pickle

def createReferencesCSV(docName):
	document = pd.read_csv(docName)
	titles = []
	references = []
	IDsToAdd = []
	yearsToAdd = []
	for i in range (len(document.title)):
		addTitle = False
		references_variants = ["References\n", "REFERENCES\n", "Rererences\n", "Reference\n", "Referenees\n"
		, "References:\n", "BIBLIOGRAPHY\n", "Iteferences:\n"]
		for variant in references_variants:
			if(variant in document.paper_text[i]):
				references.append(paper_texts[i].split(variant)[1])
				titles.append(document.title[i])
				IDsToAdd.append(document.id[i])				#it happens that for some papers we don't find the references, therefore we shouldn't add their ID in the refenceres list.
				yearsToAdd.append(document.year[i])

	dictionaryColumns = {'paper_title' : titles, 'ID':IDsToAdd, 'Year': yearsToAdd, 'references':references}
	df = pd.DataFrame(dictionaryColumns)
	df.to_csv("references.csv", sep = ',')

def createCitationsJson():
	document = pd.read_csv("references.csv")
	titles = document.paper_title
	IDs = document.ID
	references = document.references
	paper_citations = {}
	for i in range(len(titles)):
		paperFutureCitations = []
		pastAndFutureCitations = [[], paperFutureCitations]						#matrix which will contain both references for current paper and citations in the future of it
		addEntry = False
		for j in range(len(references)):										
			if (titles[i] in references[j]) and titles[j] != titles[i]:
				paperFutureCitations.append(titles[j])
				print "Paper:%s was cited in:%s" % (titles[i], titles[j])
				addEntry = True
		if(addEntry):
			paper_citations.update({titles[i]:pastAndFutureCitations})
	for keyI in paper_citations:					
		referencesOfPaper = []
		for keyJ in paper_citations:
			if keyI in paper_citations[keyJ][1]:
				referencesOfPaper.append(keyJ)
		paper_citations[keyI][0] = referencesOfPaper
	#print paper_citations
	save_obj(paper_citations, "paper_citations_dict")
	jsonObj = json.dumps(paper_citations)
	print jsonObj
def createVisualizationCsv():
	categories = returnCategoryList
	categoriesInCsv = []
	year_ranges = ["1987-1990", "1990-1993", "1993-1996", "1996-1999", "1999-2002", "2002-2005", "2005-2008", "2008-2011", "2011-2014", "2014-2017"]
	paper_citations = load_obj("paper_citations_dict")
	i = 0
	year_ranges_in_csv = []
	titles_for_visualizations = []
	levels = []
	level4 = []
	citation_count = []
	for key in paper_citations:
		if key != "Distributed " and key != "Gates":
			for year_range in year_ranges:
				if(int(year_range.split("-")[0])) <= paper_citations[key][2] and (int(year_range.split("-")[1])) >= paper_citations[key][2]:
					for citations in paper_citations[key][1]:
						level4.append(citations)	
						categoriesInCsv.append(i % 14)
						year_ranges_in_csv.append(year_range) 
						titles_for_visualizations.append(key)
						citation_count.append(1)
					i += 1
	futureDocument = {'Level1':year_ranges_in_csv, 'Level2':categoriesInCsv, 'Level3':titles_for_visualizations, 'Level4':level4, 'Total':citation_count}
	df = pd.DataFrame(futureDocument, columns = futureDocument.keys())
	df.to_csv("visualizations.csv", sep = ',')


def returnCategoryList():
	categories = []
	for i in range(6):
		categories[i] = "Category %d" % i
	return categories	
def getAverageYear(docName):
	document = pd.read_csv(docName)
	years = document.year
	avgYear = 0
	for i in range (len(years)):
		avgYear += years[i]
	print float(avgYear)/len(years)
def createYearCsv(docName):
	document = pd.read_csv(docName)
	titles = []
	IDsToAdd = []
	yearsToAdd = []
	for i in range (len(document.paper_text)):
		addTitle = False
		references_variants = ["References\n", "REFERENCES\n", "Rererences\n", "Reference\n", "Referenees\n"
		, "References:\n", "BIBLIOGRAPHY\n", "Iteferences:\n"]
		for variant in references_variants:
			if(variant in document.paper_text[i]):
				titles.append(document.title[i])
				IDsToAdd.append(document.id[i])				#it happens that for some papers we don't find the references, therefore we shouldn't add their ID in the refenceres list.
				yearsToAdd.append(document.year[i])
	columnsDic = {'paper_title' : titles, 'ID':IDsToAdd, 'Year': yearsToAdd}
	df = pd.DataFrame(columnsDic)
	df.to_csv("years.csv", sep = ',')

def save_obj(obj, file_name):
    with open(file_name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(file_name):
    with open(file_name + '.pkl', 'rb') as f:
        return pickle.load(f)
	

if __name__ == '__main__':
	#createReferencesCSV("papers.csv")
	#createYearCsv("papers.csv")
	#createCitationsJson()
	createVisualizationCsv()
	#getAverageYear("papers.csv")
