# An Analysis of Dataset Overlap on Winograd-Style Tasks
# AUTHORS: Ali Emami, Adam Trischler, Kaheer Suleman, and Jackie Cheung

# Paper link: 
https://arxiv.org/abs/2011.04767

# Abstract:

The Winograd Schema Challenge (WSC) and variants inspired by it have become important benchmarks for common-sense reasoning (CSR). Model performance on the WSC has quickly progressed from chance-level to near-human using neural language models trained on massive corpora. In this paper, we analyze the effects of varying degrees of overlap between these training corpora and the test instances in WSC-style tasks. We find that a large number of test instances overlap considerably with the corpora on which state-of-the-art models are (pre)trained, and that a significant drop in classification accuracy occurs when we evaluate models on instances with minimal overlap. Based on these results, we develop the KnowRef 60k dataset, which consists of over 60k pronoun disambiguation problems scraped from web data. KnowRef60k is the largest corpus to date for WSC-style common-sense reasoning and exhibits a significantly lower proportion of overlaps with current pretraining corpora.

# Reproduce Results

**Knowref60k** contains code for the scraping of the corpus from the text sources (as well as a README with reproduce instructions)

**Overlap_Analysis** contains that code used to analyze overlap and performance ramificiations between test and train corpora  (as well a README with more details). 
