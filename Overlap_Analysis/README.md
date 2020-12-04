# CSR Overlap Generation

This repository contains the code to generate the overlapping instances between the pre-training corpora used for BERT and RoBERTa for the CSR Benchmarks.

## Content
[`create_indexed_data.py`] contains the code to index the pretraining corpora (located in 'Raw_Corpora') into the folder 'Indexed_Corpora'

[`find_overlap.py`] contains the code to that uses the indexed corpora in 'Indexed_Corpora' along with the test sets in 'Test_sets' to generate overlapping instances into the folder 'Overlaps'

## Installation

The code was tested on Python 3.5+
Necessary to install Whoosh package (pip install whoosh)


## Usage

To reproduce the results on the unswitched version, run the following command:
```shell
python create_indexed_data.py --corpus CORPUS
```
followed by


```shell
python find_overlap.py\
  --pretraincorpus CORPUS
  --testset TEST_SET
```

This creates the overlap files, pickled as .p files.
