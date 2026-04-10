Biologists **do** look for periodic patterns in gene expression data, particularly in contexts like **circadian rhythms**, **developmental processes**, and **cell cycle regulation**. Single-cell RNA-seq (scRNA-seq) presents unique challenges due to its **irregularly sampled timepoints**, which complicate traditional time-series analysis. Below is a structured overview of the topic:

---

### **1. Periodic Patterns in Gene Expression**
- **Circadian rhythms**: Gene expression cycles with a ~24-hour period (e.g., *PER2*, *CLOCK* genes).
- **Developmental processes**: Gene expression patterns during embryonic development (e.g., *Hox* genes).
- **Cell cycle**: Cyclical gene expression during mitosis and interphase.

---

### **2. Methods for Irregularly Sampled Data**
Single-cell RNA-seq often lacks synchronized timepoints, so methods must handle **uneven sampling**. Key approaches include:

#### **A. Lomb-Scargle Periodogram**
- **Purpose**: Detect periodic signals in irregularly sampled data (e.g., circadian rhythms).
- **Usage in Genomics**:
  - Widely used in **circadian rhythm studies** (e.g., [Ko et al., 2010](https://doi.org/10.1038/nature09064)).
  **Example**: Detecting 24-hour cycles in scRNA-seq data from time-lapse experiments.
- **Advantages**: Robust to missing data, handles uneven sampling.
- **Limitations**: Assumes sinusoidal signals; may miss non-linear patterns.

#### **B. Time-Series Analysis Tools**
- **Dynamic Time Warping (DTW)**: Aligns irregular timepoints for cross-sample comparisons.
- **Wavelet Transform**: Captures both frequency and time localization (useful for transient periodicity).
- **Hidden Markov Models (HMMs)**: Model state transitions (e.g., circadian phases) with probabilistic states.

#### **C. Machine Learning Approaches**
- **Neural Networks**: Deep learning models (e.g., Temporal Convolutional Networks) can infer periodic patterns from irregular data.
- **Bayesian Methods**: Probabilistic frameworks (e.g., Stan, PyMC) for modeling uncertainty in timepoints.

#### **D. Software Tools**
- **R Packages**: 
  - `lomb` (Lomb-Scargle implementation).
  - `circa` (circadian rhythm analysis).
  - `tsibble` (for irregular time series).
- **Python Libraries**: 
  - `scipy.signal.lombscargle` (Lomb-Scargle).
  - `pyts` (time-series analysis).
- **Genomics Tools**: 
  - **Scanpy** (scRNA-seq analysis with periodicity detection).
  - **Seurat** (integrated with time-course analysis).

---

### **3. Circadian Rhythm Detection from Wearable Data**
- **Wearable Devices**: Smartwatches (e.g., Fitbit, Apple Watch) collect irregular data on activity, sleep, and physiological signals.
- **Methods**: 
  - **Lomb-Scargle** is used to detect 24-hour cycles in activity/sleep data.
  - **Machine learning models** (e.g., random forests) predict circadian phase from irregular timepoints.
- **Example**: Studies using Fitbit data to analyze circadian misalignment in shift workers.

---

### **4. Companies in This Space**
#### **Genomics & Biotech**
- **Illumina**: Provides sequencing platforms for gene expression studies.
- **10x Genomics**: Offers scRNA-seq solutions with tools for temporal analysis.
- **BGI Group**: Uses time-series analysis in developmental biology.
- **Synthego**: Develops tools for CRISPR-based gene regulation studies with temporal dynamics.

#### **Wearable Tech & Health Analytics**
- **Fitbit**: Analyzes circadian rhythms via sleep/activity data.
- **Apple**: Integrates circadian health metrics in Apple Watch.
- **Oura**: Focuses on sleep and circadian rhythm tracking.
- **Whoop**: Uses wearable data to monitor physiological rhythms.

#### **AI & Analytics Platforms**
- **Zebra Medical Vision**: Uses AI for time-series analysis in clinical data.
- **Tempus**: Analyzes longitudinal genomic data for cancer progression.

---

### **5. Challenges & Future Directions**
- **Data Integration**: Combining scRNA-seq with wearable data for multi-omics analysis.
- **Computational Efficiency**: Handling large-scale, high-dimensional time-series data.
- **Interpretability**: Translating periodic patterns into biological insights (e.g., regulatory networks).

---

### **Summary**
- **Lomb-Scargle** is indeed used in genomics, particularly for circadian rhythm detection.
- **Methods** include Lomb-Scargle, time-series analysis, and machine learning.
- **Wearable data** leverages similar techniques to detect circadian patterns.
- **Key players** span biotech, wearable tech, and AI platforms.

This interdisciplinary approach is critical for understanding dynamic biological processes and personalized health monitoring.
