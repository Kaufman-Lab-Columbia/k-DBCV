# k-DBCV

k-DBCV is an efficient python implementation of the density based cluster validation (DBCV) score proposed by Moulavi et al. (2014). The implementation leverages a k-dimensional tree to efficiently calculate intercluster distances resulting in improved performance when compared with previous implementations. 

For optimizing k-DBCV to choose parameters from commonly used density-based clustering algorithms (DBSCAN, HDBSCAN, OPTICS) we recommend looking at our DBOpt library: https://github.com/Kaufman-Lab-Columbia/DBOpt

## Getting Started
### Dependencies
- SciPy
- NumPy
### Installation
k-DBCV can be installed via pip:
```
pip install kDBCV
```

## Usage
To score clustering scenarios, the following libraries are used:
- scikit-learn
- ClustSim

For visualization:
- matplotlib
 
### DBCV Score
#### Simple Scenario
The half moons dataset simulated from scikit-learn is shown:
<p align="center">
  <img width="500" height="300" src=https://github.com/user-attachments/assets/22c7c5c3-dcf1-47d4-86fd-53f428e7f87b
</p>

```
DBCV_Score(X,labels)
```
Output: 0.5068928345037831

#### Scenario II
A larger dataset of clusters simulated with Clust_Sim-SMLM is shown:

<p align="center">
  <img width="300" height="300" src=https://github.com/user-attachments/assets/acd7adee-9416-4a61-bfa0-caebf540097b
</p>
 
```
score = DBCV_score(X,labels)
```
Output: 0.6171526846848352

### Extracting Individual Cluster Scores
k-DBCV enables individual cluster score extraction where each cluster is assigned a score without consideration for noise:
Individual Cluster Score = separation-sparseness/max(separation,sparseness)

By default, ind_clust_scores is set to False
```
score, ind_clust_score_array = DBCV_Score(X,labels, ind_clust_scores = True)
```
Individual cluster scores are displayed by color below:
<p align="center">
  <img width="350" height="300" src=https://github.com/user-attachments/assets/56cd291a-9991-45d9-8dd7-cd132ec823fb
</p>

### Memory cutoff
A memory cutoff is necessary to prevent attempts to score clusters that would exceed available memory. This cutoff should be set dependent on the machine being used. The default is set to a maximum of 25.0 GB. The score will output a -1 if the cutoff would be exceeded, along with an error message. To remove these error messages set batch_mode = True (Default is False).
```
score = DBCV_score(X,labels, memory_cutoff = 25.0)
```

## Relevant Citations
#### Density Based Cluster Validation

Moulavi, D., Jaskowiak, P. A., Campello, R. J. G. B., Zimek, A. & Sander, J. Density-based clustering validation. SIAM Int. Conf. Data Min. 2014, SDM 2014 2, 839–847 (2014)

#### k-DBCV implementation

Hammer, J. L., Devanny, A. J. & Kaufman, L. J. Density-based optimization for unbiased, reproducible clustering applied to single molecule localization microscopy. Preprint at https://www.biorxiv.org/content/10.1101/2024.11.01.621498v1 (2024)

## License
k-DBCV is licensed with an MIT license. See LICENSE file for more information.

## Referencing
#### In addition to citing Moulavi et al., if you use this repository, please cite with the following:

Hammer, J.L., Devanny, A.J. & Kaufman, L.J. Bayesian optimized parameter selection for density-based clustering applied to single molecule localization microscopy. Commun Biol 8, 902 (2025). https://doi.org/10.1038/s42003-025-08332-0

Code DOI:
![image](https://github.com/user-attachments/assets/ea5d6c65-fac4-4813-85b4-eb7938d3b839)

## Contact 
kaufmangroup.rubylab@gmail.com
