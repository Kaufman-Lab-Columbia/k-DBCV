import numpy as np
import scipy

def format_data(X,labels):

    n_samp = float(X.shape[0])

    #initial check if all data is noise
    if np.sum(labels) == -n_samp:
        return 'noise',0,0,0,0,0
       
    d=X.shape[1] 

    # Stack labels with X and sort
    relist = [i for i in X.T]
    relist.append(labels)
    Xl = np.vstack((relist)).T
    Xl_sort = Xl[Xl[...,-1].argsort()]

    # Find where clusters are seperated
    cluster_ID_split = np.where(np.diff(Xl_sort[...,-1]))[0]

    #Checks for clusters that are single or only two points, reassigns them to noise then resorts the data if necessary
    diff_arr = np.append(np.diff(cluster_ID_split), (n_samp-1)-cluster_ID_split[-1])
    idx1 = np.where(diff_arr == 1)[0]
    idx2 = np.where(diff_arr == 2)[0]
    renoise = len(idx1)+(2*len(idx2))
    if renoise > 0:
        for i in range(len(idx1)):
            Xl_sort[cluster_ID_split[idx1[i]]+1] = np.append(Xl_sort[cluster_ID_split[idx1[i]]+1][...,:-1], -1)
        for i in range(len(idx2)):
            Xl_sort[cluster_ID_split[idx2[i]]+1] = np.append(Xl_sort[cluster_ID_split[idx2[i]]+1][...,:-1], -1)
            Xl_sort[cluster_ID_split[idx2[i]]+2] = np.append(Xl_sort[cluster_ID_split[idx2[i]]+2][...,:-1], -1)     
        Xl_sort = Xl_sort[Xl_sort[...,-1].argsort()]   
        cluster_ID_split = np.where(np.diff(Xl_sort[...,-1]))[0]

    #Checks if all data is now noise
    if np.sum(Xl_sort[...,-1]) == -n_samp:
        return 'noise',0,0,0,0,0


    if Xl_sort[...,-1][0] == -1:
        cluster_sort = Xl_sort[cluster_ID_split[0]+1:,:]
        cluster_groups = np.split(cluster_sort, (cluster_ID_split-(cluster_ID_split[0]))[1:])
        cluster_ind = np.concatenate([cluster_ID_split-(cluster_ID_split[0]), [len(cluster_sort)-1]]) 
    else:
        cluster_sort = Xl_sort
        cluster_groups = np.split(cluster_sort, cluster_ID_split+1)
        cluster_ind = np.concatenate([[0],cluster_ID_split+1, [len(cluster_sort)-1]])

    N_clust = len(cluster_groups)
    if N_clust < 2:
        return 'not enough clusters',0,0,0,0,0




    return cluster_sort,cluster_groups,cluster_ind,n_samp,d,N_clust

# populate the dictionaries that store key values -> sparseness,mst etc.
def Intracluster_analysis(N_clust,cluster_groups,d,mem_cutoff=15000):

    core_dists_arr = []
    core_dists_dict = {}
    core_pts = {}
    sparseness = {}
    for i in range(N_clust):
        cluster = cluster_groups[i][:,:-1]
        cluster_length = len(cluster)

        if cluster_length > mem_cutoff:
            return 'not enough memory',0,0,0
        
        intraclustmatrix_condensed = scipy.spatial.distance.pdist(cluster, metric='euclidean') 
        all_pts_core_dists = all_points_core_distance(intraclustmatrix_condensed, d)
        all_core_dists_matrix = np.tile(all_pts_core_dists, (all_pts_core_dists.shape[0], 1))
        max_core_dist_matrix  = np.maximum(all_core_dists_matrix ,all_core_dists_matrix .T)

        intraclustmatrix = scipy.spatial.distance.squareform(intraclustmatrix_condensed)
        intraclust_MRD_matrix = np.maximum(max_core_dist_matrix ,intraclustmatrix) 
        sparseness[i],core_pts[i] = MST_builder(intraclust_MRD_matrix)
        core_dists_dict[i] = all_pts_core_dists[core_pts[i]]
        core_dists_arr.append(core_dists_dict[i])


    return sparseness,np.hstack(core_dists_arr),core_dists_dict,core_pts

def all_points_core_distance(distance_matrix_condensed, d):
    distance_matrix_condensed[distance_matrix_condensed == 0] = np.inf
    distance_matrix_condensed = (1/distance_matrix_condensed)**d
    distance_matrix = scipy.spatial.distance.squareform(distance_matrix_condensed)
    all_pts_core_dists = (distance_matrix.sum(axis=1)/(distance_matrix.shape[0] - 1))
    
    if np.sum(all_pts_core_dists)>0:
        return all_pts_core_dists**(-1/d)
    else:
        return all_pts_core_dists
    
def MST_builder(MRD_matrix):    
    MST_arr = scipy.sparse.csgraph.minimum_spanning_tree(MRD_matrix).toarray()
    if np.sum(MST_arr) == 0:
        sparseness = 0
        core_pts = np.array([0], dtype = 'int64')
    else:
        check_MST = np.hstack(np.where(MST_arr>0))
        unique_vals,index,count = np.unique(check_MST,return_counts = True,return_index = True)
        core_pts = unique_vals[count>1]
        sparseness = MST_arr[core_pts][:,core_pts].max()
        if sparseness == 0:
            sparseness = MST_arr.max()

    return sparseness, core_pts
    

def core_points_analysis(cluster_sort,cluster_ind,core_pts):
    core_pts_arr = np.array(list(core_pts.values()), dtype = object)

    if len(core_pts_arr.shape) > 1:
        core_clust_ind = np.hstack(core_pts_arr+(cluster_ind[:-1])[...,None])
    else:
        core_clust_ind = np.hstack(core_pts_arr+(cluster_ind[:-1]))

    cols = np.arange(cluster_sort.shape[1]) # changed, np.arange() is faster than range() here
    rows = core_clust_ind.astype(int)

    core_X = cluster_sort.ravel()[(cols + (rows * cluster_sort.shape[1]).reshape((-1,1))).ravel()].reshape(rows.size, cols.size)
    
    cluster_ID_split = np.where(np.diff(core_X[...,-1]))[0]+1 # to save time since this lookup appears multiple times
    core_cluster_groups = np.split(core_X[...,:-1], cluster_ID_split)
    core_X_ind = np.concatenate([[0],cluster_ID_split, [len(core_X)]]) # adjusted all indices by +1, not sure if correct or not
    
    return core_X,core_cluster_groups,core_X_ind

def intercluster_analysis(core_X,core_cluster_groups,core_X_ind,core_dists_arr,core_dists_dict):
    separation = {}

    Tree = scipy.spatial.cKDTree(core_X[:,:-1]) #KD tree of all core pts

    for i in range(len(core_cluster_groups)):
        cluster = core_cluster_groups[i]
        cluster_size = len(cluster)
        
        NN_array = Tree.query(cluster, k = cluster_size+1)
        NN_array_min = []
        for j in range(cluster_size):
            NN_array_j = np.vstack((NN_array[0][j], NN_array[1][j])).T 
            NN_array_j = NN_array_j[np.where(np.logical_or(NN_array_j[:,1].astype(int)
                                    <core_X_ind[i],NN_array_j[:,1].astype(int)>=core_X_ind[i+1]))]
            if len(NN_array_j) > 1:
                NN_array_j = NN_array_j[NN_array_j[:,0] == np.min(NN_array_j[:,0])]
            NN_array_min.append(np.hstack((NN_array_j[0],j+core_X_ind[i])))    
        NN_array_min = np.vstack(NN_array_min)
        
        min_Edists = NN_array_min[:,0]
        outer_core_pts =  NN_array_min[:,1].astype(int)
        outer_core_dists = core_dists_arr[outer_core_pts]
        inner_core_dists = core_dists_dict[i]
        
        MRD_arr = np.vstack((min_Edists,inner_core_dists,outer_core_dists)).T
        MRD_init = MRD_arr.max(axis = 1)
        init_min_MRD = np.min(MRD_init)
        MRD_det = MRD_arr.argmax(axis = 1)
        
        check_radially = np.where(np.logical_and(MRD_det==2, MRD_arr[:,0]<init_min_MRD))[0]
        if len(check_radially) == 0:
            separation[i] = init_min_MRD
        else:
            radial_check = Tree.query_ball_point(cluster[check_radially], init_min_MRD)
            for j in range(len(radial_check)):
                pts = np.array(radial_check[j])           
                outer_pts = pts[np.where(np.logical_or(pts<core_X_ind[i],pts>=core_X_ind[i+1]))]
                min_outer_core_dist = min(core_dists_arr[outer_core_pts])
                MRD_arr[check_radially[j]][2] = min_outer_core_dist

            MRD_fin = MRD_arr.max(axis = 1)
            separation[i] = np.min(MRD_fin)


    return separation

def weighted_score(sparseness,separation,N_clust,cluster_groups,n_samp, ind_clust_scores = False):
    # Add up all the weighted DBCV scores to get the total  
    
    cluster_score_set = []
    DBCV_val = 0
    for i in range(N_clust):
        cluster_validity= (
            (separation[i] - sparseness[i]) /
            max(separation[i], sparseness[i])
        )
        
        cluster_score_set.append(cluster_validity)
        cluster_size = len(cluster_groups[i])
        DBCV_val += (cluster_size/n_samp) * cluster_validity

    if ind_clust_scores == True:
        return DBCV_val, cluster_score_set  
    else:
        return DBCV_val  


            
# main function
def DBCV_score(X,labels, ind_clust_scores = False, mem_cutoff=30000):
    
    #Initially formats data for later calculations
    cluster_sort,cluster_groups,cluster_ind,n_samp,d,N_clust = format_data(X,labels)

    #Handles situations where scoring can not be performed
    if type(cluster_sort) == str:
        if cluster_sort == 'noise':
            print('All points assigned to noise')
        elif cluster_sort == 'not enough clusters':
            print('Not enough clusters: must have at least two. ')
        return -1,-1

    #Sparseness calculations for DBCV
    sparseness,core_dists_arr,core_dists_dict,core_pts = Intracluster_analysis(N_clust,cluster_groups,d,mem_cutoff)
    
    #Handles memory cutoff
    if sparseness == 'not enough memory':
        print('Memory cutoff reached: automatically assigned a score of -1. Increase mem_cutoff to attempt to score.')
        return -1,-1

    # Formats core points for intercluster analysis        
    core_X,core_cluster_groups,core_X_ind = core_points_analysis(cluster_sort,cluster_ind,core_pts)

    #Separation calculations for DBCV
    separation = intercluster_analysis(core_X,core_cluster_groups,core_X_ind,core_dists_arr,core_dists_dict)

    #DBCV score
    DBCV_val = weighted_score(sparseness,separation,N_clust,cluster_groups,n_samp, ind_clust_scores)

    return DBCV_val