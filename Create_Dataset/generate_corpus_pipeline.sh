#!/bin/bash
ACTION=$1

if [ "$ACTION" == "split" ] ; then
     python knowref_scraper/sources/split_sentences.py --mode pronoun knowref_scraper/sources/reddit knowref_scraper/sources/data/wp_pronoun_owndump.txt --n-jobs 1 --chunk-size 120
fi

if [ "$ACTION" == "postag" ] ; then
    cd stanford-postagger-full-2020-11-17
    java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile ../knowref_scraper/sources/data/wp_pronoun_owndump.txt -outputFormat slashTags -outputFile ../knowref_scraper/sources/data/wp_pronoun_owndump_pos.txt -nthreads 24
    cd ..
fi

if [ "$ACTION" == "postag_filter" ] ; then
    python knowref_scraper/sources/filter_postagged.py knowref_scraper/sources/data/wp_pronoun_owndump_pos.txt knowref_scraper/sources/data/wp_pronoun_owndump_pos_filtered_0.txt --mode pronoun --n-jobs -1
    awk '!(count[$0]++)' knowref_scraper/sources/data/wp_pronoun_owndump_pos_filtered_0.txt > knowref_scraper/sources/data/wp_pronoun_owndump_pos_filtered.txt
    rm knowref_scraper/sources/data/wp_pronoun_owndump_pos_filtered_0.txt
fi

if [ "$ACTION" == "corenlp" ] ; then
    cd stanford-corenlp-full-2018-10-05
    mkdir -p sentences
    perl -ne '/^(.*?)\|/; $_=$1; s/[_\[\]]/ /g; print "$_\n"' ../knowref_scraper/sources/data/wp_pronoun_owndump_pos_filtered.txt > wp_pronoun_owndump_inputs.txt
    split -l 100 wp_pronoun_owndump_inputs.txt sentences/wp_pronoun_owndump_
    find sentences | grep wp_pronoun_owndump_ > wp_pronoun_owndump_filelist.txt
    java -cp "*" -Xmx2048m edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -threads 32 -filelist wp_pronoun_owndump_filelist.txt
    cd ..
fi

if [ "$ACTION" == "final" ] ; then
        python  knowref_scraper/sources/filter_parsed_pronoun_knowref.py  "stanford-corenlp-full-2018-10-05/wp_pronoun_owndump_*.xml" knowref_scraper/sources/data/wp_pronoun_owndump_final_reddit.json --n-jobs 1
fi

if [ "$ACTION" == "createKnowref" ] ; then
        python  knowref_scraper/sources/create_Knowref60K_fromHash.py
fi