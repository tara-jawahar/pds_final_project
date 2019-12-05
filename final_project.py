#!/usr/bin/env python
# coding: utf-8

# In[3]:
import xlrd
import pandas as pd
import csv
import sqlite3
import matplotlib
matplotlib.use("svg")
import matplotlib.pyplot as plt
import os
if not os.environ.get("DISABLE_TESTING", False):
    get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('ggplot')
import numpy as np


# In[4]:


##Read table using pandas 
df1 = pd.read_csv("grad_rates_pupil_teacher_ratio.csv",skiprows=6)


# In[5]:


df1


# In[6]:


#create and read table using sqlite
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

#Column names end with 16 indicate school year 16-17
#Column names end with 17 indicate school year 17-18
cursor.execute("""
CREATE TABLE GRAD_RATIO(
    county_name TEXT,
    county_name_17 TEXT,
    county_name_16 TEXT,
    total_num_schools_17 INTEGER,
    total_num_schools_16 INTEGER,
    american_indian_male_17 INTEGER,
    american_indian_male_16 INTEGER,
    american_indian_female_17 INTEGER,
    american_indian_female_16 INTEGER,
    asian_male_17 INTEGER,
    asian_male_16 INTEGER,
    asian_female_17 INTEGER,
    asian_female_16 INTEGER,
    hispanic_male_17 INTEGER,
    hispanic_male_16 INTEGER,
    hispanic_female_17 INTEGER,
    hispanic_female_16 INTEGER,
    black_male_17 INTEGER,
    black_male_16 INTEGER,
    black_female_17 INTEGER,
    black_female_16 INTEGER,
    white_male_17 INTEGER,
    white_male_16 INTEGER,
    white_female_17 INTEGER,
    white_female_16 INTEGER,
    hawaiian_male_17 INTEGER,
    hawaiian_male_16 INTEGER,
    hawaiian_female_17 INTEGER,
    hawaiian_female_16 INTEGER,
    mixed_male_17 INTEGER,
    mixed_male_16 INTEGER,
    mixed_female_17 INTEGER,
    mixed_female_16 INTEGER,
    student_teacher_ratio_17 INTEGER,
    student_teacher_ratio_16 INTEGER
);""")

conn.commit()

with open ("grad_rates_pupil_teacher_ratio.csv") as grad_ratio:
    data = csv.reader(grad_ratio)
    counter = 0
    for row in data:
        if counter >= 7 and len(row)>=35:
            #print(counter)
            cursor.execute("""INSERT INTO GRAD_RATIO VALUES (?,?,?,?,?,?,?,?,?,?,
                                                             ?,?,?,?,?,?,?,?,?,?,
                                                             ?,?,?,?,?,?,?,?,?,?,
                                                             ?,?,?,?,?)""", tuple(row))
        counter += 1

        conn.commit()
            

pd.read_sql_query("SELECT * from GRAD_RATIO;", conn)


# In[7]:


#Load graduation_rate_total 
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE GRAD_RATE_TOTAL(
    region_id INTEGER,
    region_name TEXT,
    region_type TEXT,
    year INTEGER,
    variable TEXT,
    percentage REAL  
);""")

conn.commit()


with open ("graduation_rates_total.csv",encoding='latin-1') as grad_rate:
    data = csv.reader(grad_rate)
    counter = 0
    for row in data:
        if counter >= 1:
            cursor.execute("INSERT INTO GRAD_RATE_TOTAL VALUES (?,?,?,?,?,?)",tuple(row))
        counter += 1
        
conn.commit()



pd.read_sql_query("SELECT * from GRAD_RATE_TOTAL;", conn)


# In[8]:


fin_df = pd.read_excel("financial_data.xls", sheet_name=["14","15","16","17","18"], skiprow=5)
fin_df_pps = fin_df["18"].fillna(-1)


# In[9]:


# print(fin_df["18"].columns)
per_pupil_spending = pd.DataFrame([], columns=["Rank", "School System", "State", "Enrollment", "Instruction_Total", 
                              "Instruction_Salaries", "Instruction_EmployeeBenefits", "Support_Total", 
                              "Support_Pupil", "Support_Staff","Support_GeneralAdmin", "Support_SchoolAdmin"])
per_pupil_spending["Rank"] = [i for i in range(100)]
per_pupil_spending["School System"] = [i for i in fin_df_pps["Unnamed: 2"][4:] if i !="School System" and i != -1]
per_pupil_spending["State"] = [i for i in fin_df_pps["Unnamed: 3"][4:] if i !="State" and i != -1]
per_pupil_spending["Enrollment"] = [int(i) for i in fin_df_pps["Unnamed: 4"] if i != -1 and type(i) != str]
per_pupil_spending["Instruction_Total"] = [int(i) for i in fin_df_pps["Unnamed: 8"] if i != -1 and type(i) != str]
per_pupil_spending["Instruction_Salaries"] = [int(i) for i in fin_df_pps["Unnamed: 9"] if i != -1 and type(i) != str]
per_pupil_spending["Instruction_EmployeeBenefits"] = [int(i) for i in fin_df_pps["Unnamed: 10"] if i != -1 and type(i) != str]
per_pupil_spending["Support_Total"] = [int(i) for i in fin_df_pps["Unnamed: 11"] if i != -1 and type(i) != str]
per_pupil_spending["Support_Pupil"] = [int(i) for i in fin_df_pps["Unnamed: 12"] if i != -1 and type(i) != str]
per_pupil_spending["Support_Staff"] = [int(i) for i in fin_df_pps["Unnamed: 13"] if i != -1 and type(i) != str]
per_pupil_spending["Support_GeneralAdmin"] = [int(i) for i in fin_df_pps["Unnamed: 14"] if i != -1 and type(i) != str]
per_pupil_spending["Support_SchoolAdmin"] = [int(i) for i in fin_df_pps["Unnamed: 15"] if i != -1 and type(i) != str]

per_pupil_spending.to_csv(index=False)


# In[10]:


#Finance sheet 17
fin_df_percent_dist_rev = fin_df["17"].fillna(-1)


# In[11]:


percent_dist_rev = pd.DataFrame([], columns=["Rank","School System","State","Enrollment","Overall Total Percentage",
                                             "Federal Total Percentage","Federal Title I","State Total Percentage",
                                             "State General Formula Assistance","Local Total Percentage",
                                             "Local Taxes Parent Government Contributions","Other Local Government",
                                            "Charges"])

percent_dist_rev["Rank"] = [i for i in range(100)]
percent_dist_rev["School System"] = [i for i in fin_df_percent_dist_rev["Unnamed: 2"][4:] if i !="School System" and i != -1]
percent_dist_rev["State"] = [i for i in fin_df_percent_dist_rev["Unnamed: 3"][4:] if i !="State" and i != -1]
percent_dist_rev["Enrollment"] = [int(i) for i in fin_df_percent_dist_rev["Unnamed: 4"] if i != -1 and type(i) != str]
percent_dist_rev["Overall Total Percentage"] = [float(i) for i in fin_df_percent_dist_rev["Unnamed: 5"][4:] if i !="Total" and i != -1]
percent_dist_rev["Federal Total Percentage"] = [float(i) for i in (fin_df_percent_dist_rev["Unnamed: 6"]) if i !="Federal sources" and i != "Total2" and i != -1]
percent_dist_rev["Federal Title I"] = [float(i) for i in (fin_df_percent_dist_rev["Unnamed: 7"]) if i !="Federal sources" and i != "Title I" and i != -1]
percent_dist_rev["State Total Percentage"] = [float(i) for i in (fin_df_percent_dist_rev["Unnamed: 8"]) if i !="State sources" and i != "Total2" and i != -1]
percent_dist_rev["State General Formula Assistance"] = [float(i) for i in (fin_df_percent_dist_rev["Unnamed: 9"]) if i !="State sources" and i != "General" and i !="formula" and i != "assistance" and i != -1]
percent_dist_rev["Local Total Percentage"] = [float(i) for i in (fin_df_percent_dist_rev["Unnamed: 10"]) if i !="Local sources" and i != "Total2" and i != -1]

#This function changes the (Z) to zeros  
def changeZ(i):
    try:
        return (float(i))
    except:
        return(0.0)

percent_dist_rev["Local Taxes Parent Government Contributions"] = [changeZ(i) for i in (fin_df_percent_dist_rev["Unnamed: 11"]) if i !="Local sources" and i != -1 and i!="Taxes and" and i != "parent" and i != "government" and i != "contributions"]
percent_dist_rev["Other Local Government"] = [changeZ(i) for i in (fin_df_percent_dist_rev["Unnamed: 12"]) if i !="Local sources" and i != -1 and i!="Other" and i != "local" and i != "governments"]
percent_dist_rev["Charges"] = [changeZ(i) for i in (fin_df_percent_dist_rev["Unnamed: 13"]) if i !="Local sources" and i != -1 and i!="Charges"]


percent_dist_rev.to_csv(index=False)


# In[14]:


#Finance sheet 16
fin_df_expenditure = fin_df["16"].fillna(-1)
fin_df_expenditure


# In[96]:


#Finance Sheet 16
expenditure = pd.DataFrame([], columns=["Rank","School System","State","Enrollment",
                                       "Elementary_secondary Expenditure Total", "Selected Objects Salaries",
                                       "Selected Objects Employee Benfits","Instruction Salaries","Instruction Employee Benefits",
                                       "Support Services Pupil Support","Support Services Instructive Staff Support",
                                       "Support Services General Administration","Support Services School Administration",
                                       "Support Services Other and Nonspecified","Other Current Spending","Capital Outlay",
                                       "Inter-governmental","Interest On Debt"])

expenditure["Rank"] = [i for i in range(100)]
expenditure["School System"] = percent_dist_rev["School System"]
expenditure["State"] = percent_dist_rev["State"]
expenditure["Enrollment"] = percent_dist_rev["Enrollment"]
expenditure["Elementary_secondary Expenditure Total"] = [int(i) for i in fin_df_expenditure["Unnamed: 5"][np.concatenate((np.arange(4,74,1),np.arange(149,217,1)))] if i !="Total" and i != -1 and i != "Elementary-secondary expenditure"]
expenditure["Selected Objects Salaries"] = [int(i) for i in fin_df_expenditure["Unnamed: 7"][np.concatenate((np.arange(4,74,1),np.arange(149,217,1)))] if i !="For selected objects" and i != -1 and i != "Salaries and" and i != "wages"]
expenditure["Selected Objects Employee Benfits"] = [int(i) for i in fin_df_expenditure["Unnamed: 8"][np.concatenate((np.arange(4,74,1),np.arange(149,217,1)))] if i != -1 and i != "Employee" and i != "benefits"]
expenditure["Instruction Salaries"] = [int(i) for i in fin_df_expenditure["Unnamed: 10"][np.concatenate((np.arange(4,74,1),np.arange(149,217,1)))] if i != -1 and i != "Salaries and" and i != "wages"]
expenditure["Instruction Employee Benefits"] = [int(i) for i in fin_df_expenditure["Unnamed: 11"][np.concatenate((np.arange(4,74,1),np.arange(149,217,1)))] if i != -1 and i != "Employee" and i != "benefits"]
expenditure["Support Services Pupil Support"] = [int(i) for i in fin_df_expenditure["Unnamed: 5"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "Pupil" and i != "support"]
expenditure["Support Services Instructive Staff Support"] = [int(i) for i in fin_df_expenditure["Unnamed: 6"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "Instructional" and i != "staff" and i != "support"]
expenditure["Support Services General Administration"] = [int(i) for i in fin_df_expenditure["Unnamed: 7"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "General" and i != "adminis-" and i != "tration"]
expenditure["Support Services School Administration"] = [int(i) for i in fin_df_expenditure["Unnamed: 8"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "School" and i != "adminis-" and i != "tration"]
expenditure["Support Services Other and Nonspecified"] = [int(i) for i in fin_df_expenditure["Unnamed: 9"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "Other and" and i != "nonspecified"]
expenditure["Other Current Spending"] = [int(i) for i in fin_df_expenditure["Unnamed: 10"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "Other" and i != "current" and i != "spending"]
expenditure["Capital Outlay"] = [int(i) for i in fin_df_expenditure["Unnamed: 11"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "Capital" and i != "outlay"]
expenditure["Inter-governmental"] = [int(i) for i in fin_df_expenditure["Unnamed: 12"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "Inter-" and i != "governmental"]
expenditure["Interest On Debt"] = [int(i) for i in fin_df_expenditure["Unnamed: 13"][np.concatenate((np.arange(76,145,1),np.arange(220,288,1)))] if i != -1 and i != "Interest" and i != "on debt"]


expenditure.to_csv(index=False)


# In[ ]:





# In[ ]:




