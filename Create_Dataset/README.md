
## [Dataset Construction]

## Idea ##

Produce a large-scale dataset with similar properties as Winograd Schema sentences but with low overlap with current pretraining corpora.

We find sentences which have two noun phrases in them, one of which is referred to later. 

The resulting dataset may contain sentences where the original target of the reference cannot be determined anymore if for the noun phrases that are persons, they are changed to names of the same gender as the pronoun.

E.g. we pull "Kevin yelled at Melissa because he was angry" which can later be changed automatically to "Kevin yelled at Jim because he was angry"--Thus they become WSC-style, common sense requiring sentences.


## Generated Dataset location ##
The test dataset (with label and annotator information, as well as the hashed sentence) is located in knowref_scraper/sources/hashed_dataset folder. The script you will run will automatically use this hashed dataset to generate the complete Knowref60k dataset. We provide you both with a one-shot (single bash command) script, as well as a step-by-step script for debugging and transparancy.


## Preliminaries ##

The code was tested on Python 3.6.5.


**Requirements.txt**
```
pip install -r requirements.txt
```


**Stanford CoreNLP and Stanford Postagger**

Please download Stanford CoreNLP (we used stanford-corenlp-full-2018-10-05), and Stanford Postagger (we used stanford-postagger-full-2020-11-17) and place their main folders containing the .jar files in the current directory.


**NLTK Libaries** 

Some of the python files require NLTK libraries to be downloaded, which can be done using nltk.download('____') within a python console. The two libraries are 'treebank' and 'names'.

**Java Runtime**

Also, please have java runtime installed on your system (sudo apt install default-jre). We tested with openjdk 11.0.9.1 2020-11-04.



## One-shot script ##

Assuming you have installed requirements.txt, downloaded all the .bz2 reddit comments, and created folders for Stanford CoreNLP  and Postagger, you can run the entire pipeline, at once, with the following command:

   ```
   bash generate_corpus_pipeline.sh oneshot
   ```

## Step-by-Step Procedure ##

General remark: Most of the scripts use [[https://pypi.python.org/pypi/joblib][joblib]] to parallelize processing. For debugging, it is advisable to set it to one. To speed up processing, set the **--n_jobs** parameter to a value larger than one.

All steps are also accessible from **pipeline.bash**.

1. Download the source text, i.e. Reddit Comments (.bz2 files) dating inclusively between 2005-12 to 2019-12 at https://files.pushshift.io/reddit/comments/ and store them in the knowref_scraper/sources/reddit folder.
2. Use **split_sentences.py** to remove paragraphs containing lists etc., split
   sentences, and filter sentences which contain numbers, symbols, etc.
   Usage:
   
   ```
   python knowref_scraper/sources/split_sentences.py --mode {mode} {inputs_dir} {output_filename}
   ```

   where **inputs_dir** is the directory is the corpus dump and **output_filename** is a filename of your
   choosing. 

   The sentences are searched for a regular expression containing a simplified
   form of the Winograd Schema pattern, e.g.

   * **Noun1…Noun2…connective…Noun[1 or 2]**  (mode **noun**)
   * **Noun1…Noun2…connective…pronoun**  (mode **pronoun**)

   In both cases, there shouldn’t be a pronoun before the connective, to ensure
   we don’t reference a sentence from before the current one.

   We don’t want to parse the sentence for nouns yet, instead we just remove all
   words from the sentence which occur in Penn Treebank as non-nouns, and
   compile the leftover words into the candidates-regex.

   The process takes about 20 minutes using around 32 cores of **rohan**. Use
   [[http://linux.die.net/man/1/nice] to reduce effects on other users.

4. Run the [[http://nlp.stanford.edu/software/tagger.shtml#Download][Stanford POS tagger]] on the resulting set. Download it, unzip it, and use
   ```
   cd "{stanford postagger glob}"
   java -cp "**" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile {input_file} -outputFormat slashTags -outputFile {output_file}
   cd ..
   ```
   This should be done after about 10-15 minutes. There is an **-nthreads** option
   in case this is too slow.

5. The POS tags provide further information about the candidate noun phrases,
   e.g., whether there actually are nouns, whether they agree in Number, whether
   there are too many other confounding NPs, whether they differ in adjectives
   (e.g. â€œThe red car â€¦ but the green carâ€¦â€ would not be a repetition of â€œcarâ€)

   This is done by **filter_postagged.py**, Usage:
   ```
   $ python knowref_scraper/sources/filter_postagged.py [--n-jobs {N}] --mode {noun|pronoun} {postagger output file} {output_filename_temp}
   $ awk '!(count[$0]++)' {output_filename_temp} {output_filename}
   $ rm {output_filename_temp}
   ```


6. Run the [[https://stanfordnlp.github.io/CoreNLP/][CoreNLP Parser]] on the resulting set. This seems to work fastest
   (judging by CPU usage) if the input is first split into multiple files. We
   can use the **split** command to do this for us, but before, we need to remove
   information about the candidates and the pronoun substitution position from
   the output of the last script:
   ```
   $ cd "{corenlp glob}"
   $ perl -ne '/^(.*?)\|/; $_=$1; s/[_\[\]]/ /g; print "$_\n"' < {filter_postagged output} > wsc_inputs.txt
   $ split -l 100 wsc_inputs.txt sentences/sents
   $ find sentences > filelist.txt
   $ java -cp "*" -Xmx6g edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -threads 32 -filelist filelist.txt
   $ cd ..
   ```

7. Final parsing step. CoreNLP parser. It messes up in a few cases where CoreNLP and nltk disagree about sentence splitting.
   ```
      $ python knowref_scraper/sources/filter_parsed_pronoun_knowref.py "{corenlp glob}" {output filename}
   ```
   The glob is something like **stanford-corenlp-version/sents*.out**.
   This script:
   - finds the candidates, connective, and pronouns and filters through only sentences with personned noun phrases, the connective and a pronoun.
   
 8. You will now have a file containing many candidate sentences. What we did with these is randomly swapped the names with names of matching gender according to the pronoun gender, creating new, more ambigious sentences that may require world-knowledge/commonsense to solve. We used annotators to label these sentences, filtering any sentences with low annotation agreement and keeping those with high annotation agreement. These made Knowref60k. In the final step, the hashed Knowref60k is aligned with the candidate sentences outputted in step 7 to generate your copy of Knowref60k.
 ```
 $ python  knowref_scraper/sources/knowref_scraper/sources/create_Knowref60K_fromHash.py
  ```



