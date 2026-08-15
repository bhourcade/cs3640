# This is the README for A5/analysis.

A5 was developed by Benjamin Hourcade (bhourcade), Carlo Velarde (cvelarde), Logan Martin (logmartin), and Gabriel Solis (grsolis).

A5/analysis was developed by Benjamin Hourcade (bhourcade) and Carlo Velarde (cvelarde).

# Setup Requirements

### Create virtual environment

`python -m venv venv`

### Activate environment

`source venv/bin/activate`

### Install required modules

`pip3 install pandas`

`pip install openpyxl`

`pip3 install statsmodels`

`pip install matplotlib`

`pip install scikit-learn`

`pip install textstat`

`pip install textblob`

`pip install seaborn`

# Explanation of Program

### NOTE 
Due to environment set ups, one may need to reconfigure the path when it comes to opening and saving files. In the code, there are lines that can be uncommented to assist in path errors.
### RUN
Assuming there is a `data/output.json`, the extract_data.py file can run simply by `python analysis/extract_data.py`

`visualize.py` can be ran for bar graphs, but if you want the scatter plot, you must uncomment the below section and comment out the above. There are instruction in the code to clarify. 

`analyze_chart_q3.py` can be ran directly by `python analysis/analyze_chart_q3.py` once data_analsis csv table has been created from `extract_data.py`. 

## Extract_data.py Summary
The `extract_data.py` script reads a json file and creates a table based on the university json objects within the json file. For each json object, it extracts whether the privacy policy mentions ccpa_or_cpra, ferpa, or gdpr. It also executes functions to determine word length, sentiment, and reading level. Word length is determined by splitting the string of text and taking the length. The reading level is done using the *Flesch Reading Ease Formula* which gives a number between 0-100 that indicates the reading ease of the provided text. 0 is very confusing and 100 is very easy. The sentiment score is determined by *TextBlob*, which is a natural language toolkit. It returns a number between -1 and 1, where -1 is super negative and 1 is super positive. 
Once all data has been extracted and determined, a row entry is added to the pandas table. This is done for all json objects (universities). Once completed, both a csv and an excel workbook are saved to the data folder to be furthur analyzed. The output files will be found at `./data/data_analysis.csv` and `./data/data_analysis.xlsx`.
## Visualize.py and analyze_chart_q3.py Summary
`visualize.py` and `analyze_chart_q3.py` creat visualizations of the data found in the table created by `extract_data.py`. Using matplotlib, these scripts create bar graphs and scatter plots to show relationships. The `analyze_chart_q3.py` script takes the visualizations a step furthur by performing basic averages and writing the results to a txt file called `analysis_results.txt` in the data folder. Those results are then used/referenced in question 3 of the research paper. 

## data_stats.py
`data_stats.py` takes the collected data extracted from pivacy policies stored in `dnsmpi_analysis.xlsx` and `dnsmpi_data.xlsx` to compute useful statistics. 

`dnsmpi_analysis.xlsx` stores the compiled data from the privacy policies. `dnsmpi_data.xlsx` stores the manually compiled data about whether or not universities are in California and if the DNSMPI is required.

In order to collect data from `dnsmpi_analysis.xlsx` for different categories (i.e., public, private non-profit, private for-profit, and all unniversities), I utilized the pandas library. Pandas was also useful when I had to jump between `dnsmpi_analysis.xlsx` and `dnsmpi_data.xlsx` when computing statistics for the dnsmpi links.

The `summary_statistics()` method calculates the minimum, median, maximum, mean, and standard deviation for all privacy policies, public universities' privacy policies, private for-profit universities' privacy policies, and private non-profit privacy policies for the following: the proportion of privacy policies that mention the CPPA or CPRA, the proprotion that mention FERPA, the proportion that mention GDPR, the mean word length, the mean reading level, the mean sentiment index, and the proportion of privacy policies with DNSMPI links. The `statistics` module made it possible to calculate these statistics. It saves this information in `descriptive_stats.txt`.

The `pairwise_tests()` method performs pairwise tests between public universities', private non-profit universities', and private for-profit universities' privacy policies regarding the proprotion of policies that mention the CPPA or CPRA, the proportion of policies that mention FERPA, the proportion of policies that mention GDPR, the mean word length, the mean reading level, the mean sentiment index, and the proportion of privacy policies with DNSMPI links. The `statsmodels` module made this possible. The results are saved in `pairwise_tests.txt`.

The `dnsmpi_stats()` method gathers all the universities where the DNSMPI link is not required and marks them as either in California or not in California. It then retrieves the number of DNSMPI links within each group and computes the voluntary DNSMPI rate. It performs a test to test for a significant difference in the voluntary DNSMPI rate. It also displays the estimated voluntary adoption rate for both groups: California and non-California. Then, `dnsmpi_stats()` collects the universities required to have the DNSMPI links and computes a compliance rate. It identifies the universities that did not have DNSMPI links when they were supposed to and displays the hompages. All this was possible with the `pandas` and `statsmodels` modules. The results were saved in `dnsmpi_analysis.txt`.

## cluster.py
`get_data()` collects the privacy policies from `crawler.py`'s output.

The `find_optimal_k()` method removes stop words, words that appear in more than 50% of the privacy policies, and words that appear in less than 2 privacy policies. After that, it calculates a TF-IDF score for each word leftover and adds that score as an entry in a vector corresponding to each privacy policy. This was possible using the `TfidVectorizer` module. Then, it uses the `sklearn` module to compute a k-means fit for each vector. This groups vectors into k clusters based on how close they are to each other. The value of k is initially unknown so a graph showing the total squared distance from each vector to its cluster center is created for k = 1 to 10. This graph is available in `optimal_k.png`. Then, it is possible to visuallually examine the graph to see where the "elbow" is.

The `analyze_clusters()` method takes in the optimal k and clusters the privacy policies into k clusters. It makes `cluster_visualization.png` which projects the vectors onto a 2D plane and makes it easier to understand how close the vectors are to each other. Then, it makes `clusters.txt` which shows which universities are in which clusters with the help of the `pandas` module. Next, it finds the centroid or mean vector value for each cluster and picks out the entries with the highest values. In doing this, it retrieves the top 15 words with the highest TF-IDF score for each cluster. Lastly, it dsiplays the top 15 TF-IDF words for each cluster in `diction_by_cluster.txt`.

## cluster_analysis.py
It imports the `analyze_clusters()` method from `cluster.py` after determing what the optimal k is.

# Who Did What

## Benjamin Hourcade (bhourcade)
I performed a statistical analysis and tests as part of `data_stats.py`. I also made `cluster_analysis.py` which clusters privacy policies according to significant wording. Furthermore, I compiled the data manually for `dnsmpi_data.xlsx` and `dnsmpi_requirements.xlsx`. Additionally, I manually added in the privacy policies and DNSMPI links for the failures we encountered `crawler.py`'s output.

## Carlo Velarde (cvelarde)
Carlo created the `extract_data.py` file to analyze the university json objects and build a csv table. In regard to the privacy policy, the `extract_data.py` file checks for keywords, word length, sentiment score, readability score, and for the DNSMPI link.
Carlo also created the `visualize.py` and `analyze_chart_q3.py` files that create visualizations of the table built from `extract_data.py`. The visualzations show averages among university categories. 
# Useful Resources

- https://www.sitepoint.com/using-python-parse-spreadsheet-data/
  This helped me use the pandas module for reading and extracting data from an excel file.
- https://www.freecodecamp.org/news/ pandas-count-rows-how-to-get-the-number-of-rows-in-a-dataframe/
  This was useful for iteating through the excel file called data_analysis.xlxs.
- https://www.w3schools.com/python/module_statistics.asp
  This helped me generate summary statistics for data, like mean, median, and standard deviation.
- https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportions_ztest.html
  This helped me conduct a z-test for proportions.
- https://www.statsmodels.org/dev/generated/statsmodels.stats.weightstats.ttest_ind.html#statsmodels.stats.weightstats.ttest_ind
  This helped me do t-tests for population means.
- https://stackoverflow.com/questions/78630047/how-to-stop-numpy-floats-being-displayed-as-np-float64
  This helped me get rid of np.float64 before floats
- https://blog.cambridgespark.com/how-to-determine-the-optimal-number-of-clusters-for-k-means-clustering-14f27070048f
  This helped me find the optimal number of clusters to use.
- https://spotintelligence.com/2023/01/16/document-clustering-in-python/#:~:text=Grouping%20similar%20documents%20together%20in,extensive%20collections%20of%20text%20data
  This helped me vectorize a list of strings and use the best approximation method to figure out which cluster a privacy policy should fall in.
- https://medium.com/@mehdirt/mastering-text-clustering-with-python-a-comprehensive-guide-f8617f53c327#preprocessing-the-data
  This helped me visualize clusters of multidimensional vectors with color coding
- http://brandonrose.org/clustering
  This helped me present which universities were in which categories in the form of a data_frame.
- https://scikit-learn.org/0.15/auto_examples/document_clustering.html
 this helped me find the most significant words within each category. 

- https://github.com/textstat/textstat
  This helped Carlo setup and determine readability scores
  
- https://www.analyticsvidhya.com/blog/2021/10/sentiment-analysis-with-textblob-and-vader/
This helped Carlo learn and use TextBlob for sentiment analysis

- https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
This helped Carlo refresh and reference on how to make graphs using matplotlib