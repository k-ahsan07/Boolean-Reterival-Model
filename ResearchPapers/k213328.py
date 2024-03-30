#####################################   UTILITIES  ##############################################################

import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import re
import os
import json
import re
import time
nltk.download('punkt')


#################################     FUNCTION    ###############################################################


def removeSpecialCharacters(word_list):
    #return tokens that are not special character
    words = []  # to store
    for word in word_list:
        w = ''  
        for letter in word:
            # Check if the character is alphanumeric
            if letter.isalnum():  
                w += letter
        if w:
            words.append(w)
    return words



def lowercaseTokens(word_list):
    return [word.lower() for word in word_list]


def stemming(word_list):
    #use porter stemmer to stem token
    ps = PorterStemmer()
    stemmed_words = [ps.stem(word) for word in word_list]
    return stemmed_words


def removeSingleLetterWords(word_list):
    return [word for word in word_list if len(word) > 1]


def removing_url(word_list):  # to remove url
    url_pattern = re.compile(r'https?://\S+|http?://\S+|http\.\S+|www\.\S+')
    return url_pattern.sub(' ', word_list)



def read_stopwords():
    #return all tokens which are not part of stopWords
    with open("Stopword-List.txt", "r") as file:
        content = file.read()
    return content.split()


def normalize(token):
    # apply case folding
    token = removeSpecialCharacters(token)
    # apply stemming
    token = stemming(token)
    # apply remove of single letter
    token = removeSingleLetterWords(token)
    return token


def tokenizer(content):
    # Replace special characters with spaces
    content = content.replace("-", " ")
    content = content.replace(".", " ")
    content = content.replace("1", " ")
    content = content.replace("2", " ")
    content = content.replace("3", " ")
    content = content.replace("4", " ")
    content = content.replace("5", " ")
    content = content.replace("6", " ")
    content = content.replace("7", " ")
    content = content.replace("8", " ")
    content = content.replace("9", " ")
    # Tokenize the content
    words = word_tokenize(content)
    return words


def parseDoc(content, invertedIndex, doc_id):
    words = tokenizer(content)
    #apply normalization to token
    tokens = normalize(words)
    for token in tokens:
        if token not in invertedIndex:
            invertedIndex[token] = []
        if doc_id not in invertedIndex[token]:
            invertedIndex[token].append(doc_id)


def parseQuery(query):
    # tokenize the query and return tokens
    tokens = tokenizer(query)
    return tokens


def saveInvertedIndex(invertedIndex):
    #write in txt file
    with open("InvertedIndex.txt", "w") as file:
        for term, doc_ids in invertedIndex.items():
            # Convert integers to strings
            doc_ids_str = [str(doc_id) for doc_id in doc_ids]
            # write the term
            file.write(f"{term}: {' '.join(doc_ids_str)}\n")


def savePosIndex(posIndex):
    #write in txt file
    with open("PosIndex.txt", "w") as file:
        # iterate each term and positions
        for term, positions in posIndex.items():
            file.write(f"{term}: {' '.join(map(str, positions))}\n")






def loadInvertedIndex():
    #load index from txt file and return
    file_path = r"./InvertedIndex.txt" 
    invertedIndex = {}
    # Open the file and read its contents
    with open(file_path, "r") as file:
        # Read each line in the file
        for line in file:
            # Split the line into term and document IDs
            term, *doc_ids = line.strip().split(":")
            # Convert document IDs to integers
            doc_ids = [int(doc_id) for doc_id in doc_ids[0].split()]
            invertedIndex[term] = doc_ids
    return invertedIndex


def loadPosIndex():
    # Define the file path for the positional index
    file_path = r"./PosIndex.txt"
    posIndex = []
    # Open the file and read its contents
    with open(file_path, "r") as file:
        # Read each line in the file
        for line in file:
            term, *positions = line.strip().split(":")
            positions = [int(pos) for pos in positions[0].split()]
            posIndex.append({term: positions})
    return posIndex


def fetchPostingList(term, invertedIndex):
    # return postings list from the inverted index for that term
    return invertedIndex[term][1]


def fetchPositions(term, doc, posIndex):
    # return positions list for that term from that doc
    return posIndex[doc-1][term]



#######################   DOCUMENT PROCESSING       ######################################


def processDocs():
    #Load stopwords to eliminate them while processing
    posIndex = []  
    globalDict = []  
    for i in range(1, 31, 1):
        # open doc and read it
        docName = f"{i}.txt"
        doc = open("Data/"+docName, "r")
        docContent = doc.read()
        doc.close()
        #parse document and get tokens
        tokens = parseDoc(docContent)
        #generate positional index for current doc
        posIndex.append({})
        for pos in range(len(tokens)):
            token = tokens[pos]
            if token not in posIndex[i-1].keys():
                posIndex[i-1][token] = [pos]
            else:
                posIndex[i-1][token].append(pos)
            if token not in globalDict:
                globalDict.append(token)
    # sort all terms in alphabetical order
    globalDict.sort()
    invertedIndex = {}
    # initialise each words posting list as an empty list
    for word in globalDict:
        invertedIndex[word] = (0, [])
    for term in invertedIndex.keys():
        doc_freq = 0
        for docID in range(1, 31, 1):
            if term in posIndex[docID-1].keys():
                doc_freq += 1
                invertedIndex[term][1].append(docID)
        invertedIndex[term] = (doc_freq, invertedIndex[term][1])
    # save index
    saveInvertedIndex(invertedIndex)
    savePosIndex(posIndex)





######################    QUERY PROCESSING    ##############################################



def proximityQuery(tokens, invertedIndex):
    # load positional index
    posIndex = loadPosIndex()
    # get k
    k = int(tokens[3])
    terms = []
    for i in range(0, 2, 1):
        terms.append(normalize(tokens[i]))
    result = set()
    for doc in fetchPostingList(terms[0], invertedIndex):
        # make sure 2nd term also exists in that doc
        if doc not in fetchPostingList(terms[1], invertedIndex):
            continue
        list1 = fetchPositions(terms[0], doc, posIndex)
        list2 = fetchPositions(terms[1], doc, posIndex)
        l1 = 0
        l2 = 0
        # iterate over both lists
        while l1 < len(list1) and l2 < len(list2):
            # check number of words between positions of both words
            diff = list1[l1] - list2[l2]
            if diff <= k :
                result.add(doc)
                break
            # otherwise increment the iterator
            else:
                if diff > k:
                    l2 += 1
                else:
                    l1 += 1
    return result


def applyNOT(result_docs, term, invertedIndex):
    # check if term exist
    if term in invertedIndex:
        # Update the set of document IDs by removing the document IDs
        result_docs.difference_update(invertedIndex[term])
    return result_docs



def process_query_result(search_terms, operators, inverted_index, all_documents):
    # Initialize an empty set for documents containing the search terms
    documents_containing_terms = set()
    # Add documents containing the first search term to the set
    if search_terms[0] in inverted_index:
        documents_containing_terms.update(inverted_index[search_terms[0]])
    # Perform intersection, union, or exclusion operation for the remaining search terms
    for i in range(1, len(search_terms)):
        term = search_terms[i]
        if term in inverted_index:
            if operators[i - 1] == 'AND':
                documents_containing_terms.intersection_update(inverted_index[term])
            elif operators[i - 1] == 'OR':
                documents_containing_terms.update(inverted_index[term])
            elif operators[i - 1] == 'NOT':
                documents_containing_terms.difference_update(inverted_index[term])
    # Perform the NOT operation to exclude documents containing the search terms
    documents_not_containing_terms = all_documents - documents_containing_terms
    return documents_not_containing_terms







def booleanQuery(query_tokens, invertedIndex):
    # initialize empty set
    result_docs = set()
    operator = None
    for term in query_tokens:
        # Check if the term is 'NOT
        if term == 'NOT':
            # Set the operator to 'NOT'
            operator = 'NOT'
        elif term in invertedIndex:
            if operator is None:
                result_docs.update(invertedIndex[term])
            elif operator == 'AND':
                result_docs.intersection_update(invertedIndex[term])
            elif operator == 'OR':
                result_docs.update(invertedIndex[term])
            elif operator == 'NOT':
                result_docs = applyNOT(result_docs, term, invertedIndex)
                operator = None  # Reset operator after handling NOT
        else:
            operator = term
    return result_docs



data_dir = r"D:\IR\Assignment01-K213328-full\ResearchPapers\data"
invertedIndex = {}
doc_id = 1

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        match = re.search(r'\d+', filename)
        if match:
            doc_id = int(match.group())  # Extract numeric part of filename
            with open(os.path.join(data_dir, filename), "r") as file:
                content = file.read()
                content_remove = removing_url(content)
                parseDoc(content_remove, invertedIndex, doc_id)
        else:
            break

# Save inverted index
saveInvertedIndex(invertedIndex)




def printInvertedIndex(invertedIndex, query_tokens):
    # Print the inverted index
    print("\nInverted Index:")
    for term in query_tokens:
        if term in invertedIndex:
            doc_ids = invertedIndex[term]
            if isinstance(doc_ids, (list, tuple)):
                print(f"{term}: {' '.join(map(str, doc_ids))}")
            else:
                print(f"{term}: {doc_ids}")
        else:
            print(f"{term}: Not found in inverted index")


def processQuery(query):
    # Record the start time
    start_time = time.time()
    # Load inverted index for processing as it is needed in processing
    invertedIndex = loadInvertedIndex()
    # Parse query
    query_tokens = parseQuery(query)
    if len(query_tokens) > 2 and '/' in query_tokens:
        result = proximityQuery(query_tokens, invertedIndex)
    else:
        result = booleanQuery(query_tokens, invertedIndex)
    end_time = time.time()
    # Calculate the time 
    time_taken = end_time - start_time
    return result, time_taken

# # Example of boolean query
# query = input("Enter your boolean query: ")
# # Tokenize the query
# query_tokens = query.split()
# invertedIndex = loadInvertedIndex()
# # Perform boolean query
# result_docs = booleanQuery(query_tokens,invertedIndex)
# # Print the inverted index for the result of the boolean query
# printInvertedIndex(invertedIndex, query_tokens)
# # Print the resulting documents
# print("\nResulting Documents:")
# print(result_docs)
