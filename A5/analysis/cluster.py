import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

#Returns a list of unique university ids and a list of the corresponding privacy policies.
#Each id is a combination of the university link and its class (public, private for-profit, private non-profit)
def get_data():
    privacy_policies = []
    uni_ids = []
    with open('data/output.json', 'r', encoding = 'utf-8') as file:
        data = json.load(file)
        for item in data:
            if item.get('status') == True:
                url = item.get('url')
                uni_class = item.get('class')
                #If the privacy policy cannot be retrieved, this is an empty string
                privacy_policy = item.get('privacy_policy_text') or ''
                uni_id = str(url) +" ("+str(uni_class)+")"
                privacy_policies.append(privacy_policy)
                uni_ids.append(uni_id)
    return privacy_policies, uni_ids

#Returns a TF-IDF matrix with each row is a privacy policy
#and each column is a word count for a partiuclar word.
def vectorize(privacy_policies):
    #vectorizer = CountVectorizer(stop_words='english')
    #Removes words present in more than half of the privacy_policies (eg. privacy)
    #Removes words that fail to occur in at least 2 privacy policies (eg. university names)
    #Eliminates common words that are not stop words
    vectorizer = TfidfVectorizer(max_df=.5, min_df=2, stop_words='english')
    X = vectorizer.fit_transform(privacy_policies)
    return X, vectorizer

def find_optimal_k(privacy_policies):
    #The sum of the squared distances between the vector and the nearest cluster center
    #If the vector is approximated by a cluster center, this this value is just the residual sum of squares
    #The optimal number of k will minimize this value
    rss = []

    #max number of clusters we want
    k_upper = min(10, len(privacy_policies))

    #min number of clusters we want
    k_lower = 1

    #k is the number of clusters
    K = range(k_lower, k_upper)
    for k in K:
        #best approximation method for each cluster size
        #calculating and stroing the square residual distance
        km = KMeans(n_clusters = k)
        X, vectorizer = vectorize(privacy_policies)
        km = km.fit(X)
        rss.append(km.inertia_)
    
    #Plot this data
    #choose the optimal k using the elbow method
    plt.plot(K, rss, 'bx-')
    plt.xlabel('k (number of clusters)')
    plt.ylabel('Residual Sum of Squares')
    plt.title('Elbow Method For Optimal k')
    plt.savefig('analysis/optimal_k.png')
    plt.show()

#Figures out which privacy policies fall in which cluster
#An optimal k is required
def get_clusters(privacy_policies, opt_k):
    X, vectorizer = vectorize(privacy_policies)
    km = KMeans(n_clusters = opt_k, max_iter=100000)
    km.fit(X)

    #A list of numbers ranging from 0 to (k-1), 
    #indicating the cluster that the privacy-policy with the same index falls in
    #Uses best approximation method by minimizing the distance between
    #the privacy policy vector and the subspace formed by the vectors in the cluster.
    y_pred = km.predict(X)
    labels = km.labels_
    return y_pred, labels, km, X, vectorizer

#This plots/projects the vectors onto a 2D-plane where each cluster is color coded
def visualize_clusters(privacy_policies, opt_k, labels, X):
    #reduces the dimensions of the matrix to 2 for visualization
    X_pca = PCA(n_components = 2).fit_transform(X.toarray())
    plt.figure(figsize=(10,5))
    plt.scatter(X_pca[:,0],X_pca[:,1], c=labels, cmap = 'viridis', s= 2)
    plt.title('K-Means Clusters')
    plt.savefig('analysis/cluster_visualization.png')
    plt.show()

#Creates a data frame such that each row
#has an entry for the university id and the cluster number
def frame_clusters(privacy_policies, uni_ids, opt_k, labels):
    clusters = labels.tolist()
    policy_dict = {'university': uni_ids, 'cluster': clusters}
    cluster_frame = pd.DataFrame(policy_dict, columns = ['cluster', 'university'])
    return cluster_frame

#Once, an optimal k has been found, the clusters are analyzed
#Graphs and files are generated
def analyze_clusters(privacy_policies, uni_ids, opt_k):
    y_pred, labels, km, X, vectorizer = get_clusters(privacy_policies, opt_k)
    visualize_clusters(privacy_policies, opt_k, labels, X)
    cluster_file(privacy_policies, uni_ids, opt_k, labels)
    diction_file(privacy_policies, opt_k, km, X, vectorizer)

#This displays which universities are in each cluster
def cluster_file(privacy_policies, uni_ids, opt_k, labels):
    s = ""
    cf = frame_clusters(privacy_policies, uni_ids, opt_k, labels)
    for group in range(opt_k):
        s += "Cluster #"+str(group+1)+"\n"
        for row in range(len(privacy_policies)):
            if (cf['cluster'].iloc[row] == group):
                s += cf.iloc[row]['university'] + "\n"
    cluster_file = open("analysis/clusters.txt", "w")
    cluster_file.write(s)

#Finds the most significant words
#Significant words are words that maximize their TF-IDF index
#They also must not appear in more than 50% of the privacy policies
#Plus, they need to occur in at least two privacy policies
def diction_file(privacy_policies, opt_k, km, X, vectorizer):
    s = ""
    sorted_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for group in range (opt_k):
        s += "Cluster #"+str(group+1)+"\n"
        for i in sorted_centroids[group, :15]:
            s += terms[i] +" "
        s += "\n"
    diction_file = open("analysis/diction_by_cluster.txt", "w")
    diction_file.write(s)

def main():
    privacy_policies, uni_ids = get_data()
    find_optimal_k(privacy_policies)
    
if __name__ == "__main__":
    main()
