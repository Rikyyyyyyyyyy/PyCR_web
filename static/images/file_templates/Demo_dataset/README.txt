--------------------
GENERAL INFORMATION
--------------------

1. Title of Dataset: 

Replication Data for: Global Metabolome Analysis of Dunaliella teriolecta, Phaeobacter italicus R11 Co-cultures using Thermal Desorption - Comprehensive Two-dimensional Gas Chromatography - Time-of-Flight Mass Spectrometry (TD-GC×GC-TOFMS) 

2. Author Information

	A. Principal Investigator Contact Information
		Name: Michael Sorochan Armstrong
		Institution: University of Alberta
		Email: mdarmstr@ualberta.ca

3. Date of data collection (single date, range, approximate date): 

2019-09-01

4. Geographic location of data collection: 

Edmonton, Alberta, Canada

5. Information about funding sources that supported the collection of the data: 

The authors wish to acknowledge the support of the Natural Sciences and Engineering Research Council of Canada (NSERC) and the support given to The Metabolomics Innovation Centre (TMIC) through grants from Genome Alberta, Genome Canada, and the Canada Foundation for Innovation. A*STAR SFS IAF-PP grant A20H7a0152 awarded to Rebecca Case also enabled this research.

---------------------------
SHARING/ACCESS INFORMATION
---------------------------

1. Licenses/restrictions placed on the data: 

These data are available under a Creative Commons Public Domain Dedication (CC0 1.0) license <https://creativecommons.org/publicdomain/zero/1.0/> 

2. Links to publications that cite or use the data: 

Preprint of the study results
https://doi.org/10.1101/2021.09.27.461748 

3. Was data derived from another source? yes/no

Raw data was processed and aligned using ChromaTOF v4.72

4. Recommended citation for this dataset: 

Sorochan Armstrong, M. (2021). Replication Data for: Global Metabolome Analysis of Dunaliella teriolecta, Phaeobacter italicus R11 Co-cultures using Thermal Desorption - Comprehensive Two-dimensional Gas Chromatography - Time-of-Flight Mass Spectrometry (TD-GC×GC-TOFMS). Federated Research Data Repository. https://doi.org/10.20383/102.0510

---------------------------
METHODOLOGICAL INFORMATION
---------------------------

1. Description of methods used for collection/generation of data: 

	The data was collected on a Comprehensive Two-dimensional Gas Chromatograph - Time-of-Flight Mass Spectrometer (GC×GC-TOFMS). The samples are algal, bacterial, and co-culture samples that were prepared under controlled conditions with the aim of examining metabolic differences between the different sample classes. Metabolites were extracted from the sample using a modified version of the method proposed by Bligh and Dyer (Bligh, E. Graham, and W. Justin Dyer. "A rapid method of total lipid extraction and purification." Canadian journal of biochemistry and physiology 37.8 (1959): 911-917.) for fatty acid extraction, dried, and derivatised using a methoxymation step, before trimethylsilylation using methyl-N-(trimethylsilyl)trifluoroacetamide (MSTFA). The liquid solution containing the derivatised extracts as well as the derivatisation reagents were introduced into a thermal desorption unit to vent the excess solvent before being introduced into the instrument via a disposable microvial insert within the same thermal desorption unit.

2. Methods for processing the data: 

	The data were processed using LECO ChromaTOF version 4.72. Baseline offset for peak detection was adjusted by a factor of 1.2 above the baseline noise. Anticipated peak widths were determined via a survey of the total ion current (TIC) of 10 characteristic peaks. The authors opted to cater the data analysis parameters towards smaller peaks, since it has been shown to be difficult to integrate small peaks and large peaks together using the same data analysis parameters. The expected peak shape parameters were 10 seconds for the first dimension retention times, and 0.1 seconds for the second dimension retention times. Second dimension sub-peaks were integrated if the deconvolved mass spectra exceeded a relative match factor of at least 650. Subpeaks with a SNR less than 6 were not integrated.

	Peaks were integrated into the aligned peak table if 5 or more apexing masses were present, and the signal-to-noise ratio (SNR) of the base peak for each feature was above 15. Peaks across multiple samples were associated with each other if they fell within 2 modulation periods of each other along the first dimension retention time, or within 0.2 seconds along the second dimension.
	
3. Instrument- or software-specific information needed to interpret the data: 

	The samples were collected on a LECO Pegasus 4D system, using a quad-jet dual-stage cryogenic modulator. The data is presented in the raw data files as a matrix of m x n observations and n mass channels. The data was collected at 200 observations/second (Hz), and a modulation period of 2.5 seconds was used. The modulation period describes the length of the second dimension separation, and can be used to infer the 3 dimensional structure of the data from the matrix information presented in the raw data. 
	
	The raw data was exported from the proprietary .peg file format using the loadpeg function created by Robin Abel. The software is available at https://doi.org/10.5281/zenodo.4035154

4. Standards and calibration information, if appropriate: 

	Fully untargeted analysis; no standards were run to confirm the identity of each component.

5. Environmental/experimental conditions: 

	First dimension column: 60 m length x 0.25 mm internal diameter with 0.25 um film thickness Rxi-5SilMS stationary phase. Second dimension column: 1.4 m length x 0.25 mm internal diameter with 0.25 um film thickness Rtx-200MS stationary phase. The initial oven temperature was set at 80 C, held for 4 minutes and ramped at 3.5 C/minute to a maximum oven temperature of 315 C with a 10 minute final hold. The secondary oven offset relative to the temperature of the first dimension oven was + 10 C, with a modulator offset of + 15 C. The mass spectrometer collected spectra from 40 to 800 m/z at 200 spectra/second. Electron ionisation energy was -70 eV. Ion source temperature was held at 200 C, with a transfer line temperature of 300 C. An acquisition delay of 650 seconds was utilised to preserve the integrity of the mass spectrometer filament until after any residual solvent had been purged from the instrument.

6. Describe any quality-assurance procedures performed on the data: 

	Replicate samples were run to ensure the consistent results at every stage of the sample preparation. They are designated by the sample code, followed by "R" in the data. The sensitivity and mass accuracy of the mass spectrometer was calibrated internally at regular intervals (data unavailable), and the retention times were monitored visually throughout the entire experiment.

7. People involved with sample collection, processing, analysis and/or submission: 

	Michael Sorochan Armstrong, Oscar Rene Arredondo Campos, Catherine C. Bannon, A. Paulina de la Mata, Rebecca Case, James J. Harynuk

-----------------------------------------------------------------
DATA-SPECIFIC INFORMATION
-----------------------------------------------------------------

1. Number of variables:

3256

2. Number of samples:

75

3. Missing data codes:

        Code/symbol        0
