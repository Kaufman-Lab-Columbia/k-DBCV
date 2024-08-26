# Draft-DBCV

DBCV* is an efficient python implementation of the density based cluster validation (DBCV) score proposed by Moulavi et al. (2014). 

## Getting Started
### Dependencies
- SciPy
- NumPy
### Installation
DBCV* can be installed via pip:
```
pip install ....?
```
or
```
pip install ....?
```

## Usage
To score clustering scenarios, the following libraries are used:
- scikit-learn
- Clust_Sim-SMLM

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
A larger dataset of clusters simulated with Clust_Sim-SMLM are shown:
<p align="center">
  <img width="400" height="300" src=https://github.com/user-attachments/assets/acd7adee-9416-4a61-bfa0-caebf540097b
</p>
```
score = DBCV_Score(X,labels)
```
Output: 0.6171526846848352

### Extracting Individual Cluster Scores
DBCV* enables individual cluster score extraction where each cluster is assigned a score:
Individual Cluster Score = Sep-Sparse/Sep

By default, ind_clust_scores is set to False
```
score, ind_clust_score_array = DBCV_Score(X,labels, ind_clust_scores = True)
```
Individual cluster scores are visualized by color below:
<p align="center">
  <img width="300" height="300" src=https://github.com/user-attachments/assets/56cd291a-9991-45d9-8dd7-cd132ec823fb
</p>

### Memory cutoff
Currently, DBCV* memory scales with the number of points in an individual cluster. A memory cutoff is necessary and should be set dependent on the machine being used. The default is set to a maximum of 15000 points allowed in a single cluster. The score will output an error when an individual cluster exceeds this cutoff.
```
score = DBCV_Score(X,labels, memory_cutoff = 10)
```
Output: 

## Relevant Citations
#### Density Based Cluster Validation

Moulavi, D., Jaskowiak, P. A., Campello, R. J. G. B., Zimek, A. & Sander, J. Density-based clustering validation. SIAM Int. Conf. Data Min. 2014, SDM 2014 2, 839–847 (2014)

#### DBCV* implementation
...Our citation here

## License
DBCV* is licensed with an MIT license. See LICENSE file for more information.

## Referencing
#### In addition to citing Moulavi et al., if you use this repository, please cite:
...Our citation here

## Contact 

