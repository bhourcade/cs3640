import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

import cluster

def main():
    #Manually determine what the optimal k-value is
    opt_k = 7
    privacy_policies, uni_ids = cluster.get_data()
    cluster.analyze_clusters(privacy_policies, uni_ids, opt_k)
    
if __name__ == "__main__":
    main()