# cyber-threat-analysis-using-LLM

[![threat analysis](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/html_images/distro.png)](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/helper_functions.py)

In this project, we have used various NLP techniques including entity analysis.

For a better viewing experience, please follow these steps:

1. **Download all zip files and the HTML page to your computer.**
2. **Unzip the "html_images.zip" file**, and optionally, unzip the "codes_and_data.zip" file as well.
3. **Run the HTML file to access the interactive page.**

On the HTML page:
- Click on the green buttons at the bottom to view the design diagrams for each phase and sub-phase of the project.
- Clicking on these diagrams will direct you to the corresponding implementation code on GitHub.
- Click on the blue buttons on the right side of the page to access the GitHub link for the relevant data in each phase.

The overall project can be divided into five phases:

## Exploratory Data Analysis (EDA)

In this phase, we conducted exploratory data analysis to understand the structure and patterns in the data.

[![EDA Diagram](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/html_images/eda.png)](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/preprocess.py)

## A. Initial data cleaning:

Here the URLs (saved in a csv file) was processed to extract raw text data using Requests and Beautiful Soup. Then, they were minimally cleaned mainly removing longer words, MD5 codes, etc. No other processing were done at this stage to preserve the context of the data.

[![Phase A Diagram](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/html_images/cleaning.png)](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/data_cleaning.ipynb)

## B. Smaller sentence creation

In this phase using the cleaned data from phase (A), sentence tokens were created. They were further broken into smaller chunk sizes, cleaned for spaces and too small size chunks etc. These smaller sentence-like chunks are further refined based on the relevant keywords for atp29. Finally refined sentences are saved in a text file.

[![Phase B Diagram](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/html_images/sentence_refining.png)](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/apt_analysis.ipynb)

## C. Meaningful sentence creation using GPT2:

In this phase the refined sentences from phase (B) were used to create a collection of meaningful sentences, that can be used for pattern analysis and threat hunting. For this, gpt2 based tokenizer and gpt2 LMH model were used. Also attention masks and token ids were used in this processing. Finally these meaningful sentences are saved in another text file to use.

[![Phase C Diagram](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/html_images/sentence_generation.png))](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/apt_analysis.ipynb)

## D. MITRE ATT&CK framework analysis:
In this phase MITRE framework website was accessed and cleaned similar to the procedure mentioned in (A). Then, sentences are refined using the same process mentioned I (B). Then these sentences are processed to extract polarity sentiment scores. Finally, based on thresholding these scores, we divided these MITRE sentences in threat, action and info.

[![Phase D Diagram](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/html_images/mitredata_thresholded.png)]([code_link](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/mitre_analysis.ipynb))

## E. Embedding creation, matching and APT29 attack solution database creation

In this phase, we used GloVe twitter 100 pre-trained model to create embeddings of MITRE sentences and as well as meaningful sentences about APT29. One crucial step is, MITRE sentences were further transformed into documents to reduce processing time. Finally, cosine similarity was applied to compare these embeddings with each other (the document embeddings from MITRE and sentence embedded from apt29). Based on these matching, APT29 sentences are finally added to three final categories: 

1. Threat advisory 
2. Hunting action 
3. General information.

[![Phase E Diagram](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/html_images/final.png)](https://github.com/shubha07m/cyber-threat-analysis-using-LLM/blob/main/mitre_analysis.ipynb)


## Next step:

A next step to this could be use these labeled data about APT29 vulnerability analysis to fine tune or even retrain any standard LLM model. This step would require much more amount of data and computation resources, specifically GPU.
