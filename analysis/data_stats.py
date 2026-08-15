#Importing the pandas module to read an xlsx file
import pandas as pd

import statistics

import sys

import numpy as np

#Eliminates having np.float64 before floats
np.set_printoptions(legacy='1.25')

from statsmodels.stats.proportion import proportions_ztest

from statsmodels.stats.weightstats import ttest_ind

#Opening excel workbook xlsx file
#This works when analysis/data_stats.py is run from the A5 directory
#rather than from the /analysis directory
workbook = pd.read_excel('./data/data_analysis.xlsx')
dnsmpi_wb = pd.read_excel('./data/dnsmpi_data.xlsx')

#Due to differences in operating systems, use
#workbook = pd.read_excel('./data/data_analysis.xlsx')

#Returns the rows in the table that correspond to a particular group of universities
#The three groups of universities are public, private non profit, and private for profit
def get_uni_groups():

    #public universitiesc
    pub = []

    #public non profit universities
    pnp = []

    #public for profit universities
    pfp = []

    for index in range (len(workbook)):
        #Gets university group of a partiuclar row
        group = workbook['Kind of university'].iloc[index]
        if group == 'Public':
            pub.append(index)
        elif group == 'Private Non-Profit':
            pnp.append(index)
        elif group == 'Private For Profit':
            pfp.append(index)
        else:
            print("Error in data_analysis.xlsx")
            sys.exit()

    #range(len(workbook)) returns all the indices in the workbook table
    return range(len(workbook)), pub, pnp, pfp

def get_vol_dnsmpi_rates():
    cali_unis_nrq, not_cali_unis_nrq = get_dnsmpi_nrq()
    vol_unis_cali, vol_unis_not_cali = get_voluntary_DNSMPI_unis()
    ov_rate = (len(vol_unis_cali) + len(vol_unis_not_cali))/(len(cali_unis_nrq) + len(not_cali_unis_nrq))
    cal_rate = len(vol_unis_cali)/len(cali_unis_nrq)
    not_cal_rate = len(vol_unis_not_cali)/len(not_cali_unis_nrq)
    s="Estimated overall voluntary DNSMPI link adoption rate among American universities\n"
    s+=str(len(vol_unis_cali) + len(vol_unis_not_cali))+"/"+str(len(cali_unis_nrq) + len(not_cali_unis_nrq))+" = "+str(round(ov_rate,3))+"\n"
    s+="Estimated voluntary DNSMPI link adoption rate among American universities in California\n"
    s+=str(len(vol_unis_cali))+"/"+str(len(cali_unis_nrq))+" = "+str(round(cal_rate,3))+"\n"
    s+="Estimated voluntary DNSMPI link adoption rate among American universities outside of California\n"
    s+=str(len(vol_unis_not_cali))+"/"+str(len(not_cali_unis_nrq))+" = "+str(round(not_cal_rate,3))
    return s

#Gets data for the proportion of universities with voluntary dnsmpi links
#inside and outside of California
def get_dnsmpi_data():
    cali_unis_nrq, not_cali_unis_nrq = get_dnsmpi_nrq()
    vol_unis_cali, vol_unis_not_cali = get_voluntary_DNSMPI_unis()
    vol_dnsmpi_cali = []
    vol_dnsmpi_not_cali = []

    #Generating data for unis in california that voluntarily have DNSMPI links
    for cal in cali_unis_nrq:
        if cal in vol_unis_cali:
            vol_dnsmpi_cali.append(1)
        else:
            vol_dnsmpi_cali.append(0)

    #Generating data for unis not in california that voluntarily have DNSMPI links
    for not_cal in not_cali_unis_nrq:
        if not_cal in vol_unis_not_cali:
            vol_dnsmpi_not_cali.append(1)
        else:
            vol_dnsmpi_not_cali.append(0)
    return vol_dnsmpi_cali, vol_dnsmpi_not_cali

#Retreives the universities in California and not in California 
#where the DNSMPI is not required
def get_dnsmpi_nrq():
    cali_unis_nrq = []
    not_cali_unis_nrq = []
    for i in range (len(workbook)):
        uni = workbook['University link'].iloc[i]
        uni_mask = dnsmpi_wb['University link'] == uni

        #Finding university with the same name in dnsmpi_data.xlsx
        uni_mask = dnsmpi_wb['University link'] == uni
        temp_wb = dnsmpi_wb.loc[uni_mask]

        #Checking for a mismatch in dataframes
        if (temp_wb.empty):
            print(uni+" is in data_analysis.xlsx but not in dnsmpi_data.xlsx")
            sys.exit()
        if (len(temp_wb) > 1):
            print("Multiple copies of "+uni+" in dnsmpi_data.xlsx")
            sys.exit()

        #The dataframe should only have one row
        #Checking if the DNSMPI is required
        if (temp_wb['DNSMPI required'].iloc[0] == 0):

            #Checking if the uni is in California
            if (temp_wb['California'].iloc[0] == 1):
                cali_unis_nrq.append(uni)
            else:
                not_cali_unis_nrq.append(uni)
    return cali_unis_nrq, not_cali_unis_nrq

#Gets the universities that voluntarily have DNSMPI links
def get_voluntary_DNSMPI_unis():
    vol_unis_cali = []
    vol_unis_not_cali = []
    for i in range (len(workbook)):
        uni = workbook['University link'].iloc[i]

        #Finds universities that have the DNSMPI link
        if (workbook['DNSMPI'].iloc[i] == 1):

            #Finding university with the same name in dnsmpi_data.xlsx
            uni_mask = dnsmpi_wb['University link'] == uni
            temp_wb = dnsmpi_wb.loc[uni_mask]

            #Checking for a mismatch in dataframes
            if (temp_wb.empty):
                print(uni+" is in data_analysis.xlsx but not in dnsmpi_data.xlsx")
                sys.exit()
            if (len(temp_wb) > 1):
                print("Multiple copies of "+uni+" in dnsmpi_data.xlsx")
                sys.exit()

            #The dataframe should only have one row
            #Checking if the link is voluntary
            if (temp_wb['DNSMPI required'].iloc[0] == 0):
                #University is in California
                if (temp_wb['California'].iloc[0] == 1):
                    vol_unis_cali.append(uni)
                else:
                    vol_unis_not_cali.append(uni)
    return vol_unis_cali, vol_unis_not_cali

#Retrieves the universities required to have the DNSMPI link
def get_rq_dnsmpi_unis():
    rq_unis = []
    for i in range (len(workbook)):
        uni = workbook['University link'].iloc[i]

        #Finding university with the same name in dnsmpi_data.xlsx
        uni_mask = dnsmpi_wb['University link'] == uni
        temp_wb = dnsmpi_wb.loc[uni_mask]

        #Checking for a mismatch in dataframes
        if (temp_wb.empty):
            print(uni+" is in data_analysis.xlsx but not in dnsmpi_data.xlsx")
            sys.exit()
        if (len(temp_wb) > 1):
            print("Multiple copies of "+uni+" in dnsmpi_data.xlsx")
            sys.exit()
        
        #The dataframe should only have one row
        #Checking if the link is voluntary
        if (temp_wb['DNSMPI required'].iloc[0] == 1):
            rq_unis.append(uni)
    return rq_unis

#Gets the number of universities that fail to have a DNSMPI link when required
def get_defiant_unis():
    def_unis = []
    rq_unis = get_rq_dnsmpi_unis()
    for uni in rq_unis:

        #Finding university with the same name in data_analysis.xlsx
        uni_mask = workbook['University link'] == uni
        temp_wb = workbook.loc[uni_mask]

        #Check for mismatch in data frames
        if (len(temp_wb) > 1):
            print("Multiple copies of "+uni+" in data_analysis.xlsx")
            sys.exit()
        
        #Checking if the dnsmpi link exists
        if (temp_wb['DNSMPI'].iloc[0] == 0):
            def_unis.append(uni)
    
    compliance_rate = (len(rq_unis) - len(def_unis))/len(rq_unis)
    return def_unis, rq_unis, compliance_rate


#Retrieves data from a particular category for a specific university group
def get_data(category, indices):
    data = []
    for index in indices:
        value = workbook[category].iloc[index]
        if category in ['CCPA or CPRA', 'FERPA', 'GDPR', 'Word length', 'DNSMPI']:
            value = int(value)
        elif category in ['Reading level', 'Sentiment index']:
            value = float(value)
        data.append(value)
    return data

#Returns a summary of the given data
#This summary consists of the minimum, median, maximum, mean, and standard deviation of the data
def data_summary(data):
    if len(data) == 0:
        print("Error: no data")
        sys.exit()
    #Checks if data is numeric
    if not isinstance(data[0], (int, float)):
        print("Data is not numeric")
        sys.exit()
    return round(min(data),3), round(statistics.median(data),3), round(max(data),3), round(statistics.mean(data),3), round(statistics.stdev(data),3)

#For every group of universities specified, summary statistics for each category are displayed
def summary_statistics(indices, groups, categories):
    s = ""
    #Iterates over all groups
    for i in range(len(groups)):
        group = groups[i]
        if i != 0:
            s += "\n"
        s += "Summary statistics for "+str(group)+"\n"
        obs = len(indices[i])
        s+="Number of observations: "+str(obs)+"\n"

        #Iterates over all categories
        for cat in categories:
            try:
                #Summary statistics for this particular category and group
                mn, med, mx, mean, std = data_summary(get_data(cat, indices[i]))
                s+= str(cat)+": min = "+str(mn)+", med = "+str(med)+", max = "+str(mx)+", mean = "+str(mean)+", stdev = "+str(std)+"\n"
            except:
                print("Error: There needs to be at least two universities for each university group.")
                sys.exit()
    return s

#Returns the correct test to use depending on what category is being tested
def get_test(cat):
    #Qualitative varaibles can be interpreted as a proportion when averaged over a group
    #Hence, a two-sample z-test for a difference in population proportions is required
    if cat in ['CCPA or CPRA', 'FERPA', 'GDPR', 'DNSMPI']:
        return "z-test"

    #These categories' values are quantitative and not qualitative in nature
    #Therefore, a two-sample t-test for a difference in population means is needed
    elif cat in ['Word length', 'Reading level', 'Sentiment index']:
        return "t-test"

    else:
        print("Error in data_analysis.xlsx")
        sys.exit()

def run_test(data1, data2, test, alpha):
    #Compares proportions
    if test == 'z-test':

        #Standard deviation is 0 for both sets of data
        #Checks for a binary split, which implies irrefutable significance
        if (statistics.stdev(data1) == 0 and statistics.stdev(data2) == 0):
            if (data1[0] == data2[0]):
                #Both sets of data have exactly the same values
                pval = 1.0
            else:
                #Both sets of data have completely different nonvariable values
                pval = 0.0

        #The standard deviation of one group is 0
        #Checks if the variable group is significantly different from the mean of the nonvaraible group
        #Does this with a one-sample Z-test
        elif ((statistics.stdev(data1) != 0 and statistics.stdev(data2) == 0) or (statistics.stdev(data1) == 0 and statistics.stdev(data2) != 0)):
            if (statistics.stdev(data1) != 0):
                count = sum(data1)
                obs = len(data1)
                value = data2[0]
            else:
                count = sum(data2)
                obs = len(data2)
                value = data1[0]
            stat, pval = proportions_ztest(count, obs, value)

        #Both sets of data are variable
        else:
            #Obtaining necessary input parameters for the z-test
            count1 = sum(data1)
            count2 = sum(data2)
            obs1 = len(data1)
            obs2 = len(data2)
            count = [count1, count2]
            obs = [obs1, obs2]
            try:
                stat, pval = proportions_ztest(count, obs)
            except:
                print("Error in generating z-test")
                sys.exit()

    #Compares means
    elif test == 't-test':
        try:
            stat, pval, df = ttest_ind(data1, data2)
        except:
            print("Error in generating t-test")
            sys.exit()
    else:
        print("Error in specifying a statistical test")
        sys.exit()

    #If p-value <= alpha-level, then there is a significant difference
    if (pval <= alpha):
        sig = True
    else:
        sig = False

    #Rounding to 3 decimal places
    pval = round(pval,5)
    return pval, sig

def dnsmpi_test(alpha):
    data_c, data_nc = get_dnsmpi_data()
    test = "z-test"
    p, r = run_test(data_c, data_nc, test, alpha)
    s="Two-sample z-test for a significant difference in the proportion of volunary DNSMPI link adoption among American universities\n"
    s+="Alpha level: "+str(alpha)+"\n"
    s+="California - Non-California: P-value = "+str(p)+", Significant = "+str(r)
    return s

#Iterates through each category and performs a test between each pair of groups
def pairwise_tests(indices, groups, categories, alpha):
    pub = indices[1]
    pnp = indices[2]
    pfp = indices[3]
    s = ""
    for cat in categories:
        test = get_test(cat)
        data_pub = get_data(cat, pub)
        data_pnp = get_data(cat, pnp)
        data_pfp = get_data(cat, pfp)
        s+="Pairwise "+str(test)+" for a significant difference in the "
        if cat == "DNSMPI":
            s+="proportion of policies that have DNSMPI links"
        elif test == "t-test":
            s+="mean "+str(cat)
        elif test == "z-test":
            s+="proportion of policies that mention "+str(cat)
        s+=" among American universities\n"
        s+="Alpha level: "+str(alpha)+"\n"
        p1, r1 = run_test(data_pub, data_pnp, test, alpha)
        p2, r2 = run_test(data_pub, data_pfp, test, alpha)
        p3, r3 = run_test(data_pnp, data_pfp, test, alpha)
        s+="Public - Private non profit: P-value = "+str(p1)+", Significant = "+str(r1)+"\n"
        s+= "Public - Private for profit: P-value = "+str(p2)+", Significant = "+str(r2)+"\n"
        s+= "Private non profit - Private for profit: P-value = "+str(p3)+", Significant = "+str(r3)
        if (cat != categories[-1]):
            s+="\n\n"
    return s

def compliance_stats():
    def_unis, rq_unis, compliance_rate = get_defiant_unis()
    s = ""
    s += "Compliance rate among American universities required to have a DNSMPI link\n"
    s += str(len(rq_unis) - len(def_unis))+"/"+str(len(rq_unis))+" = "+str(compliance_rate)+"\n\n"
    if not def_unis:
        s += "All universities investigated were compliant with DNSMPI obligations"
    else:
        s += "The following "+str(len(def_unis))+" universities did not fulfill DNSMPI obligations\n"
        for uni in def_unis:
            s += uni+"\n"
    return s


def dnsmpi_stats(alpha):
    s=""
    s += get_vol_dnsmpi_rates() + "\n\n"
    s += dnsmpi_test(alpha)+"\n\n"
    s += compliance_stats()
    return s

#Generayes analysis files (descriptive_stats.txt and pairwise_tests.txt)
#These files contain summary statstics over all groups and pairwise tests between groups for each category
def analysis_files():
    #Indices corresponding to each tow under a certain university group
    indices = get_uni_groups()

    #The groups that will be analysis with summary statistics
    summary_groups = ["total selected universities", "public universities", "private non profit universities", "private for profit universities"]
    
    #The groups that will be compared to each other with respect to a particular category
    test_groups = ["public universities", "private non profit universities", "private for profit universities"]
    
    #Listed categories
    categories = ["CCPA or CPRA", "FERPA", "GDPR", "Word length", "Reading level", "Sentiment index", 'DNSMPI']
    
    #The standard alpha level
    alpha=.05

    #Retrieving summary statistics and writing to descriptive_stats.txt
    summary_output = summary_statistics(indices, summary_groups, categories)
    summary_file_name = "analysis/descriptive_stats.txt"
    summary_file = open(summary_file_name, "w")
    summary_file.write(summary_output)

    #Retrieving test results and writing to pairwise_tests.txt
    test_output = pairwise_tests(indices, test_groups, categories, alpha)
    test_file_name = "analysis/pairwise_tests.txt"
    test_file = open(test_file_name, "w")
    test_file.write(test_output)

    dnsmpi_output = dnsmpi_stats(alpha)
    dnsmpi_stats(alpha)
    dnsmpi_file_name = "analysis/dnsmpi_analysis.txt"
    dnsmpi_file = open(dnsmpi_file_name, "w")
    dnsmpi_file.write(dnsmpi_output)

def main():
    analysis_files()

if __name__ == "__main__":
    main()


