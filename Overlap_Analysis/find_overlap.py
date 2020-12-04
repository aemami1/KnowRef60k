# -*- coding: utf-8 -*-
 
import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import sys

from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh import qparser

from whoosh.collectors import TimeLimitCollector, TimeLimit

import pickle

import csv
from tqdm import tqdm

from whoosh.collectors import TimeLimitCollector, TimeLimit
from nltk import word_tokenize,pos_tag


 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract Predicates from datasets.')
    parser.add_argument("--testset", type=str, choices=["dpr", "wsc273",
                        "winogrande", "knowref", "wsc-web"], required=True)
    parser.add_argument("--pretraincorpus", type=str, choices=["bookcorpus", "wikipedia",
                        "stories", "openwebtext", "cc-news"], required=True)    

    params = parser.parse_args()

    ix = open_dir("Indexed_Corpora/"+params.pretraincorpus)
     

    with open("Test_sets/benchmarks/"+params.testset+"/test.tsv") as fp:
        reader = csv.reader(fp, delimiter="\t")
        index=0
        indexStore=0
        for row in reader:
            if index>0 and index%2!=0:
                indexStore=indexStore+1
            index=index+1


    fullSentence=['' for _ in range(indexStore)]
    taggedSentence=[[] for _ in range(indexStore)]
    predicateSet=[[] for _ in range(indexStore)]
    otherSet=[[] for _ in range(indexStore)]
    sentenceToBeParsed=['' for _ in range(indexStore)]
    query=[set() for _ in range(indexStore)]

    with open("Test_sets/benchmarks/"+params.testset+"/test.tsv") as fp:
        reader = csv.reader(fp, delimiter="\t")
        index=0
        indexStore=0
        for row in reader:
            if index>0 and index%2!=0:
                sent1=row[1]
                sent2=row[2]
                boostScore=1
                fullSentence[indexStore]=sent1+sent2
                tokenized=word_tokenize(sent1+sent2)
                tagged=pos_tag(tokenized)

                taggedSentence[indexStore]=tagged
                indexStore=indexStore+1
            index=index+1



    listOfAuxVerbs=["is","get","gets","was","were","can","could","did","does","have","may","might",
                    "should","will","would","had","are","has","been","being", "must", "ought to", 
                    "shall", "do","having", "be","got"]

    for i in range(0,len(taggedSentence)):
        for j in range(0,len(taggedSentence[i])):
            component=taggedSentence[i][j][0]
            tag=taggedSentence[i][j][1]
            if 'n\'t' in tag:
                tag[tag.index('n\'t')-1:tag.index('n\'t')]=[''.join( tag[tag.index('n\'t')-1:tag.index('n\'t')])]

            if tag[0]=='V' or tag=='MD'  or tag=="JJ" or component=='n\'t':
                if tag!="RB":
                    predicateSet[i].append(component)
                else:
                    predicateSet[i][-1]=predicateSet[i][-1]+component


            elif tag!="NNP":
                if component!='.': 
                        otherSet[i].append(component)
        predicateSet[i].reverse()
        otherSet[i].reverse()

    #og = qparser.OrGroup.factory(0.99)

    for i in range(0,len(taggedSentence)):
        sentenceToBeParsed[i]="(\""
        while(len(predicateSet[i])!=0):
            if len(predicateSet[i])!=1:
                    sentenceToBeParsed[i]+=predicateSet[i].pop()+ " "
            else:
                    sentenceToBeParsed[i]+=predicateSet[i].pop()+"\"~10') AND ("


        while(len(otherSet[i])!=0):
            if len(otherSet[i])!=1:
                    sentenceToBeParsed[i]+=otherSet[i].pop()+ " OR "
            else:
                    sentenceToBeParsed[i]+=otherSet[i].pop()+")"         

        query[i]=QueryParser("content",ix.schema).parse(sentenceToBeParsed[i])


    # Top 'n' documents as result
    #topN = 2
    overlaps=[set() for _ in range(indexStore)]
    overlapCount=0
    with ix.searcher() as searcher:
        # Get a collector object


        print("Finished loading searcher")
        for i,k in zip(range(0,len(fullSentence)),tqdm(range(len(overlaps)))):
            c = searcher.collector(limit=50,terms=True)
            # Wrap it in a TimeLimitedCollector and set the time limit to 10 seconds
            tlc = TimeLimitCollector(c, timelimit=120.0)
             
            # Try searching
            
            try:
                searcher.search_with_collector(query[i], tlc)
            except TimeLimit:
                print("Search took too long, aborting!")
            results=tlc.results()

            #results = searcher.search(query, terms=True,limit=10)
        
            #results= searcher.search(query,limit=10)
            if results.scored_length()>0:
                overlapCount+=1
                for j in range(0,results.scored_length()):
                    if j==0:
                        print(fullSentence[i])
                        print(sentenceToBeParsed[i])
                        print("Top evidence sentence:")
                        print(results[j]['content'])
                        print(results[j].score)
                        numberOfOverlaps=len(results[j].matched_terms())
                        numberOfComponents=len(query[i].all_terms())
                        print("Number of component overlap: "+str(numberOfOverlaps))
                    overlaps[i].add((results[j]['content'],fullSentence[i],results[j].score,numberOfOverlaps,numberOfComponents,query[i]))
                print("")
            else:
                print("")


    print("Overlap count from "+params.pretraincorpus+" to "+params.testset+":" + str(overlapCount))
    with open("Overlaps/overlaps_"+params.pretraincorpus+"_"+params.testset+".p", 'wb') as fp:
        pickle.dump(overlaps, fp)
