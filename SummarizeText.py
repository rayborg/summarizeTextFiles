# coding: utf-8

# In[1]:

import bs4 as bs  
import urllib.request  
import re
import os
import nltk

#nltk.download('punkt')
#nltk.download('stopwords')

def summarize(article):
   
    #Read in file
    with open(article, 'r') as myfile:
        article_text=myfile.read()
        
    #Fix new lines and broken words
    article_text = re.sub(r'-\n', '', article_text)
    article_text = re.sub(r'\n', ' ', article_text)
    
    # Removing Square Brackets and Extra Spaces
    #article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
    article_text = ''.join([i for i in article_text if not i.isdigit()])
    article_text = re.sub(r'\s+', ' ', article_text)  

    #Fix unrecognized fi characters
    article_text = re.sub(r'\(cid:12\)', 'fi', article_text)
    
    
    # Removing special characters and digits
    formatted_article_text = re.sub(r'[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  

    #Convert text to sentences (Tokenize)
    sentence_list = nltk.sent_tokenize(article_text)  

    #Find Weighted Frequency of Occurrence
    #Remove stopwords
    stopwords = nltk.corpus.stopwords.words('english')

    #Calculate word frequencies
    word_frequencies = {}  
    for word in nltk.word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    if not word_frequencies:
        return ""
    else:
        maximum_frequncy = max(word_frequencies.values())
        

    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    #Calculating Sentence Scores
    sentence_scores = {}  
    for sent in sentence_list:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    #Summarize and print
    import heapq  
    summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)  

    return summary

if __name__ == '__main__': 
    #Pass filenames to function and get a summary of the article
    directory = os.fsencode("./text")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"): 
            fullPathFilename="./text/"+filename
            print(filename)
            summary = summarize("./text/"+filename)
            print(summary)
            print("\n\n")

            continue
        else:
            continue    
            
    #summary = summarize()
    
    #Single example
    #summary = summarize("/home/raymond/Desktop/all/text/A big data framework for intrusion detection in smart grids using apache spark.pdf.txt")
    #print(summary)
