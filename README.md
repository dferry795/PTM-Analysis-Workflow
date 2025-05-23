# Identifying Candidate PTM Sites for Cancer Drug Discovery
Created by Darian Ferry, Eric Upton-Rowley, Tessa (Bass) Tolson, and Hailey (Johnson) Zimmerman, April 2025.

Mentored by Dr. Josh Anderson

## Introduction
*This is the workflow for our 2025 Senior Bioinformatics Capstone project at Brigham Young University. 
This project is a collaboration with the Huntsman Cancer Institute.
Below are detailed steps for reproducibility.* 

## First: Downloading data
We downloaded raw data from two websites, TCGA data from the National Cancer Institute (https://portal.gdc.cancer.gov/) as well as PTM disrupting mutational data (https://ptmd.biocuckoo.cn/download.php).

The TCGA data shows the most frequent mutations across all cancer types. This data is called ***TCGA_Frequent_Mutations.tsv*** and is located in the data/ directory of this github.

The PTM disrupting data shows all mutations which disrupt a PTM across the genome. This data is called ***PTM_Disrupting_Mutations.csv*** and is located in the data/ directory of this github.

Lastly, make sure to download the **idmap.xlsx** in the data/ directory. This is an ID conversion between the uniprot IDs in the TCGA data and the regular gene name in the PTMD database. This file will help us merge these two files together.

Feel free to download these two data files directly from this github in the data/ directory to begin.

## Second: Inner join TCGA and PTM Disrupting data in R
Next, in R, we want to join these two dataframes so we can analyze the most frequent mutations (according to TCGA) which are also PTM disrupting (according to PTMD).

Go to the **StepTwoCode/** directory. Inside is a file called **Step2Code.qmd**. This is a quarto document written in R. Open this document in R or Rstudio to follow along (although RStudio has an easier GUI and is recommended). This script uses the three downloaded files from the first step to join the dataframes and also plots the PTM mutational frequency data. Inside you will find a step by step process and code chunks to run one at a time. Follow this code to see how we joined the dataframes and plotted mutational frequencies to decide our best candidate proteins.

The joined PTM disrupting mutation frequency output of this step is in the **output/** directory. It is called **Mutation_Frequency_Count.csv**. This is the expected output dataframe from this step. Feel free to download this CSV if you want to skip step 2 and go onto step 3.

## Third: Filter PTM Disrupting data by IDR and PS
We filtered the joined data, keeping only PTMs found within Intrinsically Disordered Regions (IDRs) and Phase Separation (PS) regions.

All programs for this step are in the StepThreeCode/ directory.

Verified IDRs were downloaded from DisProt: https://disprot.org/download
We downloaded the 2024_12 release, all datasets, all aspects, including ambiguous.
The data type was regions, and was downloaded as a tsv file.
This file is in the data/ directory and is called ***DisProt_release_2024_12.tsv***  
The IDR scripts also use the output of Step 2, which can be found as ***output/Mutation_Frequency_Count.tsv***

IDRs were predicted using AIUPred (https://aiupred.elte.hu/) as an API integrated into the program ***filter_idr_api.py***  
To run filter_idr_api.py, include the required argument "-m ../output/Mutation_Frequency_Count.tsv" or equivalent. Optional arguments allow you to specify output file name and DisProt file path.  
To include output file name: "-o ./MutFreq_in_IDR.tsv".  
To include DisProt file path: "-v ../data/DisProt_release_2024_12.tsv".  
The examples given for the optional arguments are the default values used if not specified as an argument.  
The output of filter_idr_api.py can be found in ***output/MutFreq_in_IDR.tsv***

**PS prediction:**  
We created a file with UniProt IDs using ***get_ids.py***.  If using a different dataset with more proteins, split the file so no file has more than 9,000 names.  
To run get_ids.py, include the required argument "-m ../output/Mutation_Frequency_Count.tsv".  You may optionally include a name for the output file using the agrument "-o ./uniprot_ids.txt".  The output of get_ids.py can be found in ***output/uniprot_ids.txt***  
We submitted the ID file(s) to https://www.uniprot.org/id-mapping to create FASTA files with protein sequences for each ID, mapping IDs from UniProtKB AC/ID to UniProtKB.  Some IDs may not map on the first try and may need to be run separately and with different settings.  Download FASTA file(s) by clicking "Download", select "Download all", and choose the canonical FASTA format.  This file can be found at ***data/idmapping_sequences.fasta***  
The mapped IDs could also be filtered to only include IDs found in the file MutFreq_in_IDR.tsv, in which case you would change the first argument to "-m ../output/MutFreq_in_IDR.tsv".  
Once IDs are mapped to protein sequences, the FASTA file(s) are submitted to ParSe (https://stevewhitten.github.io/Parse_v2_FASTA/).
In this dataset, one ID will fail to parse: **Q8WXI7**. This protein sequence exceeds the 10,000 amino acid limit for ParSe. When searched on PhaSePred (http://predict.phasep.pro/), Q8WXI7 does not appear to have phase separation regions.  
ParSe output is downloaded by scrolling to the bottom of the results page and downloading the "Predicted PS IDRs FASTA". The file can be found at ***data/PS_predictions.fasta***

The IDR-filtered file can be filtered for PTMs also in PS using the program ***filter_IDR_by_PS.py***  
To run filter_IDR_by_PS.py, include the required arguments "-p ../data/PS_predictions.fasta -d ../output/MutFreq_in_IDR.tsv" and optional argument "-o ./MutFreq_in_IDR_and_PS.tsv".  
The output of filter_IDR_by_PS.py can be found in ***output/MutFreq_in_IDR_and_PS.tsv***


## Fourth: Plotting IDRs and Cancer-Associated, PTM-Disrupting Mutation Frequency

Two main sources were used for plotting the disorder of proteins: DisProt (verified IDRs, https://disprot.org/download) and AIUPred (predicted IDRs and the confidence of the prediction, https://aiupred.elte.hu/). If the verified regions and predicted regions contradicted each other, we prioritized the verified data. One example of this is KRAS. AIUPred predicts no IDRs in KRAS; however, there are verified IDRs in KRAS from DisProt. We prioritized DisProt data because the data are verified. 

For this reason, we suggest starting Step 4 with the `Plotting_Mutations_and_IDRs_with_DisProt.qmd` file. Within this module, you will be able to see whether there is data in DisProt for the protein you are interested in.

As for an overview of the code files in the `/StepFourCode` directory in this repository, there are three `.qmd` files, each of which you can open in R or RStudio.
Here are the three files:

- `Plotting_IDRs_with_AIUPred.qmd`
- `Plotting_Mutations_and_IDRs_with_AIUPred.qmd`
- `Plotting_Mutations_and_IDRs_with_DisProt.qmd`

Each of the files show disorder and allow you to select specific genes, PTM sites, and portions of the protein to zoom in on if you would like. Only the second and third files plot mutation frequency alongside IDRs.

The first file provides plots of **only** the predicted disorder for genes that you select (not the mutation frequency). This file uses no external data that you will need to download because it depends solely on data from the UniProt (https://www.uniprot.org/api-documentation/uniprotkb) and AIUPred (https://aiupred.elte.hu/help) APIs. However, you will need to have the UniProt IDs for each gene that you would like to plot. You can find the UniProt ID for a gene/protein by looking it up in the search bar of UniProtKB (https://www.uniprot.org/) and selecting the correct gene/protein (human of course). For example, P01116 is the UniProt ID for KRAS.

The second file provides plots of the frequency of cancer-associated, PTM-disrupting mutations and whether they are within **predicted disordered regions**. This file depends on the file `Mutation_Frequency_Count.tsv`, that you will not find in the data directory. This is because the file is produced as a result of running `Step2Code.qmd` and obtaining the resulting data frame. The code to obtain a `.tsv` file containing the resulting data frame is available within `Step2Code.qmd`. If you have not run `Step2Code.qmd`, then you can simply download this file from the `/output` directory.

The third file likewise provides plots of the frequency of cancer-associated, PTM-disrupting mutations and whether they are within **verified disordered regions**. This file depends on the file `Mutation_Frequency_Count.tsv`, that you will not find in the data directory. This is because the file is produced as a result of running `Step2Code.qmd` and obtaining the resulting data frame. The code to obtain a `.tsv` file containing the resulting data frame is available within `Step2Code.qmd`. If you have not run `Step2Code.qmd`, then you can simply download this file from the `/output` directory. This `.qmd` file also depends on the `DisProt_release_2024_12.tsv`, which you can find in the `/data` folder of this repository. We suggest trying out this file first to see if your protein of interest has any **verified** data in DisProt before resorting to AIUPred, as AIUPred data only provide a prediction.

If you would like to see examples of what the plots look like for each file, there are example plots for each file in the `/output/StepFourExamplePlots` directory.

Please be aware that when you run code that creates multiple plots at once that they will not appear in the `.qmd` notebook, but they will be either in your working directory or in your Downloads folder for your viewing.

## Fifth: Using Chimera to plot 3-dimensionality

To finish the workflow, we use UCSF ChimeraX for visual analysis. To begin, download the ChimeraX software by visiting https://www.cgl.ucsf.edu/chimerax/download.html, clicking the option that works best with your operating system, and installing the software via the .dmg file you obtain from this site.

Before launching ChimeraX, go to the UniProt website at https://www.uniprot.org and search for your gene of interest. From the list of results, click on the entry that matches your target. On the left-hand menu, select “Sequence & Isoforms,” then click the “Copy sequence” button located above the amino acid sequence box.

Next, go to https://alphafoldserver.com and sign in using your Google account. Paste the copied sequence into the appropriate input box, save the job, and click “Continue and Preview Job.” When the job is complete, click the three dots to the right of the job and download the results. After downloading, unzip the file.

Now open the ChimeraX software. In the Home tab, click the “Open” button under the File section and navigate to the folder containing the unzipped AlphaFold results. Select the file that ends in “model_0.cif” to load the predicted protein structure. For improved visualization, you can also change the background color by clicking the white square under the Background section of the Home tab.

To label our PTM sites of interest, we selected the site using the “select /a: (PTM position)” command. We labeled the PTM site using the “label /a: (PTM site command)” command and colored it pink using the “color /:a (PTM site) pink” command. We also labeled frequent mutation sites of interest using the same label command and color it red using the “color /:a (mutation site) red” command. We then labeled the distance between the mutation sites and the PTM sites by using the “distance /a:(PTM site)@(associated atom) /a:(mutation site)@(associated atom)” command.

some different commands to help you asses 3d space:  
"_color bfactor palette alphafold_"  
"_show /a:100_ (whatever position you want to look at)"  
"_distance /a:100@NZ /a:105@CB (whichever distance you want to look at)"
