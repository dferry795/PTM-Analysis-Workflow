# PTM-Analysis-Workflow
Created by Darian Ferry, Eric Upton-Rowley, Tessa Bass, and Hailey (Johnson) Zimmerman, April 2025.

Mentored by Dr. Josh Anderson

## Introduction
*This is the workflow for our 2025 Senior Bioinformatics Capstone project at Brigham Young University. 
This project is a collaboration with the Huntsman Cancer Institute.
Below are detailed steps for reproducibility.* 

## First: Downloading data
We took raw data from two websites, TCGA data from the National Cancer Institute (https://portal.gdc.cancer.gov/) as well as PTM disrupting mutational data (https://ptmd.biocuckoo.cn/download.php).

The TCGA data shows the most frequent mutations across all cancer types. This data is called ***TCGA_Frequent_Mutations.tsv*** and is located in the data/ directory of this github.

The PTM disrupting data shows all mutations which disrupt a PTM across the genome. This data is called ***PTM_Disrupting_Mutations.csv*** and is located in the data/ directory of this github.

Lastly, make sure to download the **idmap.xlsx** in the data/ directory. This is an ID conversion between the uniprot IDs in the TCGA data and the regular gene name in the PTMD database. This file will help us merge these two files together.

Feel free to download these two data files directly from this github in the data/ directory to begin.

## Second: Inner join TCGA and PTM Disrupting data in R
Next, in R, we want to join these two dataframes so we can analyze the most frequent mutations (according to TCGA) which are also PTM disrupting (according to PTMD).

Go to the **StepTwoCode/** directory. Inside is a file called **Step2Code.qmd**. This is a quarto document written in R. Open this document in R or Rstudio to follow along. This script uses the three downloaded files from the first step to join the dataframes and also plots the PTM mutational frequency data. Inside you will find a step by step process and code chunks to run one at a time. Follow this code to see how we joined the dataframes and plotted mutational frequencies to decide our best candidate proteins.

## Third: Filter PTM Disrupting data by IDR and PS
We filtered the joined data, keeping only PTMs found within Intrinsically Disordered Regions (IDRs) and Phase Separation (PS) regions.

All programs for this step are in the StepThreeScripts/ directory.

Verified IDRs were obtained from DisProt: https://disprot.org/download
We downloaded the 2024_12 release, all datasets, all aspects, including ambiguous
The data type was regions, and was downloaded as a tsv file
This file is in the data/ directory and is called ***DisProt_release_2024_12.tsv***

**Predicted IDRs were obtained in two ways:**  
First, IDRs were predicted using RIDAO: https://ridao.app/
We created a file with UniProt IDs using get_ids.py then split the file so no one file had more than 9,000 names.
To run get_ids.py, include the required argument "-m path/mutation_frequency.file" and optional argument "-o path/output.file".  
We submitted these files to https://www.uniprot.org/id-mapping to create FASTA files with protein sequeces for each ID, mapping IDs from UniProtKB AC/ID to UniProtKB.
These mapping settings do not necessarily work for all IDs, but will work for most.
We mapped any failed IDs individually.
Download FASTA files by clicking "Download", select "Downlaod all", and choose FASTA format.  
The FASTA files created from https://www.uniprot.org/id-mapping were submitted as separate batches to https://ridao.app/
RIDAO provides a file for each protein, which were consolidated into one directory.
This directory is the data/protein_scores/ directory.
Filtration can be done using these scores with the ***filter_idr_predicted.py*** program.
To run filter_idr_predicted.py, include the required argument "-m path/mutation_frequency.file" and optional arguments "-o path/output.file -p path/predicted_scores/ -v path/DisProt_release_2024_12.tsv".

Second, as a faster option, we predicted IDRs using AIUPred (https://aiupred.elte.hu/) as an API integrated into the program ***filter_idr_api.py***  
To run filter_idr_api.py, include the required argument "-m path/mutation_frequency.file" and optional arguments "-o path/output.file -v path/DisProt_release_2024_12.tsv".

Both of these programs should run in 10-20 minutes.
The output of each program is nearly identical.  
The output file of filter_idr_predicted.py is in data/ directory as ***MutFreq_in_IDR_pred.csv***  
The output file of filter_idr_api.py is in data/ directory as ***MutFreq_in_IDR_api.csv***

**PS prediction:**  
UniProt IDs were pulled using the program get_ids.py  
The IDs were mapped using https://www.uniprot.org/id-mapping as in the previous step.  
Though we performed IDR and PS analysis separately, the PS analysis could be performed later using the mapped IDs from IDR.
The mapped IDs could also be filtered to only include IDs found in the file MutFreq_in_IDR_pred.csv  
Once IDs are mapped to protein sequences, the FASTA file(s) are submitted to ParSe (https://stevewhitten.github.io/Parse_v2_FASTA/).
ParSe output is downloaded by scrolling to the bottom of the results page and downloading the ***Predicted PS IDRs FASTA***.

The file MutFreq_in_IDR_pred.csv or MutFreq_in_IDR_api.csv can be filtered for PTMs also in PS using the program ***filter_IDR_by_PS.py***  
To run filter_IDR_by_PS.py, include the required arguments "-p path/phase_separation.file -d path/MutFreq_in_IDR.file" and optional argument "-o path/output.file".  
The output file of filter_IDR_by_PS.py is in data/ directory as ***MutFreq_in_IDR_and_PS.csv***


## Fourth: Plotting IDR along with mutations

## Fifth: Using Chimera to plot 3-dimensionality
**EDIT AND FINISH THIS SECTION:**

download chimera (and how to)

search up gene in uniprot, click "sequence" on the left side and then hit copy sequence

log into alphafold server, paste sequence in job, wait for job to load

hit three dots on right of job, download it

go into chimera, open the "model_0.cif" file from your alphafold job download

change background to white in chimera 

some different commands to help you asses 3d space:
_color bfactorpalette alphafold_
_show /a:100_ (whatever position you want to look at)
_distance /a:100 /a:105_ (whichever distance you want to look at)
