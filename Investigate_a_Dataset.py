
# coding: utf-8

# # Project: Investigate FBI Gun Data
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# Post Question:
# 
# 1.What census variable or fact value is most associated with high gun per capita per state? Ceusus data includes state as variable, and there are 65 differnt census measurement as value of Fact. 
# 
# 2.Which states have had the highest growth and the lowest growth in gun registrations from Apr 2010 to Jul 2016? 
# 
# 3.What is the overall trend of gun purchases by year or by year and month?

# In[16]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

census = pd.read_csv('U.S. Census Data.csv')
gun = pd.read_excel('gun_data.xlsx')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# ### General Properties

# In[17]:


#Step 1: Check data type of columns in gun data 
gun.info()


# Based on the info function of gun data, the number of rows for gun data is 12485.There is no rows with all nan value since there are several columns with 12485 entries.
# 
# There are a lot of missing values in many columns, for example, 'permit_recheck',
# 'other','rentals_handgun','rentals_long_gun','private_sale_handgun','private_sale_long_gun', 'private_sale_other'.The missing needs to be replace with mean per column.
# 
# Lastly but not least, the number of guns should be integer instead of float since gun can not be counted as 0.5. The data type should be converted from float to int.

# In[18]:


#Step 2: Check if there is any duplicated rows.
sum(gun.duplicated()) #There is no duplicated rows in gun data


# In[19]:


sum(census.duplicated()) #There is no duplicated rows in census data
#No need to remove duplicate rows 


# In[20]:


#Step 3: Check the data type of columns in census
census.info()


# In[21]:


#Find out what kind of data are in the state columns.
census.head(3)


# In[22]:


# Check the Fact Note's number of NaN values 
census['Fact Note'].isnull().sum().sum() #This returns an integer of the total number of NaN values


# Findings: Based on result of info() and head(), we can see the data type of these state columns are string, but they actually contains number and percentage.
# The string data needed to be converted into numeric type for grouping and calculation in data exploring step.
# Also,from the result, 'Fact Note' has 49 nan value, out of 65 rows, which should be considered removed to reduce the missing values for census data.

# ### Data Cleaning 
# Step 1: Replace the Nan field with mean of each column for gun data 
# 
# Step 2: Drop fact Note column since it is not used and will affect groupby function.
# 
# Step 3: Convert data type from string to float for all the state column in Census data
# 
# Step 4: Extract Year and months column based on Month in Gun data

# In[23]:


#Step 1: Replace the Nan field with mean of each column for gun data  
gun= gun.fillna(gun.mean(), axis=0, inplace=True)


# In[24]:


#check the result of replacing in Census data
gun.isnull().sum().sum() #This returns an integer of the total number of NaN values, 0 is right


# In[25]:


#Step 2: Drop fact Note column since it is not used and will affect groupby function.
census =census.drop('Fact Note',axis=1)


# In[26]:


#check the result of replacing in Census data
census.isnull().sum().sum() #0 is right answer


# In[27]:


#Step 3: Convert data type from string to float for all the state column in Census data
#Assign state to a list 
states=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
       'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',  
        'Hawaii', 'Idaho', 'Illinois','Indiana', 'Iowa', 'Kansas', 
        'Kentucky', 'Louisiana', 'Maine','Maryland', 'Massachusetts', 
        'Michigan','Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
       'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
       'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon','Pennsylvania', 
        'Rhode Island', 'South Carolina','South Dakota', 'Tennessee', 'Texas', 'Utah', 
        'Vermont','Virginia', 'Washington', 'West Virginia','Wisconsin', 'Wyoming']


# In[30]:


# For the column name in states list, remove all the non digit character and convert it to float
for state in states:
    census[state].replace(regex=True,inplace=True,to_replace=r'\D',value=r'')
    # remove all the non digit character
    census[state]=pd.to_numeric(census[state], downcast='float', errors='ignore')
    #convert data type to float and ignore the nan value
    #Using census.dtypes to check result, The result shows all the state columns's data type now is float32. 


# In[31]:


#Step 4: Extract Year and months column based on Month in Gun data
# and convert data type from string to numeric 
#Assign the data before '-' in month column to year column 
gun['year']=gun['month'].apply(lambda x: x.split("-")[0]).astype(int)
gun['year'].unique()


# In[32]:


#Assign the data after '-' in month column to year column
gun['months'] = gun['month'].apply(lambda x: x.split("-")[1]).astype(int)
gun['months'].unique()


# In[33]:


gun.head(1) # Check year and months columns are added in the gun data


# In[34]:


#step 4: Change all float columns to int since the count of gun should be integer 
#Assign columns name  to a list 
cols = ['permit', 'permit_recheck', 'handgun','long_gun','other','admin','prepawn_handgun','prepawn_long_gun',            
'prepawn_other','redemption_handgun', 'redemption_long_gun','redemption_other','returned_handgun','returned_long_gun' ,          
'returned_other','rentals_handgun', 'rentals_long_gun', 'private_sale_handgun' , 'private_sale_long_gun',        
'private_sale_other', 'return_to_seller_handgun',  'return_to_seller_long_gun','return_to_seller_other']

#Convert the column name in cols list into int64 format using applymap
gun[cols] = gun[cols].applymap(np.int64)

#Using gun.info() to check result, the result shows all the gun columns' data type are now int64


# <a id='eda'></a>
# ## Exploratory Data Analysis
# ### Research Question 1 : What census data is most associated with high gun per capita? 
# The gun and census data are divided by state with United state.  High gun per capita should also be calculated by state, except {'District of Columbia','Guam','Mariana Islands','Puerto Rico','Virgin Islands'}. these states' gun total is missing or zero.
# Among all the state, Kentucky has the highest gun per capita on Jul 2016 and Apr 2010 data.
# Kentucky,Indiana,Illinois,West Virginia,Montana are the top 5 state who have highes gun per capita on Jul 2016.
# 
# also, based on the scatter plot for all the fact value in one figure and group by column name scatterplot,there is no strong association between any fact value and  high gun per capita.
# 
# However, based on the scatter plot for fact varible and gun per capita, separately, there is some weak association found as following; 
# the positive association between gun per capita and variables which includes:
#     'White alone, percent, July 1, 2016,  (V2016)',
#     'Persons 65 years and over, percent, April 1, 2010',
#     'Owner-occupied housing unit rate, 2011-2015',
#     
# the negative association between gun per capita and variables which includes:
#     Asian alone, percent, July 1, 2016,  (V2016)
#     Foreign born persons, percent, 2011-2015 
#     Median gross rent, 2011-2015
# 

# Situation:
# In order to calculate gun per capita,  the gun totals and population for each state needed to be fetched at first, and the gun and census data needed to be combined. 
# Also, I notice the state in census data is divided as 50 columns, however, in gun data, state is only one columns which has 46 different state value. 
# Furthermore, In census data-fact column, there are all kinds of census measurement for state, for example, Population estimates, July 1, 2016,  (V2016) and Population estimates base, April 1, 2010,  (V2016). These two variable can be used for comparing data on 2010 and 2016 and fact column will be used to analyse association between gun per capital and these census measurement.
# 
# Solution:
# Therefore, the 1st step is to transpose the census data to make state value in one columns, then summarize gun totals by year 2010 and 2016 since there are 2010 and 2016 population number in census data, then merge gun 2010 and 2016 summary with transposed census data by state column, lastly calculate the gun per capita and list the highest Top 5 gun per capital states in 2016 and 2010. 
# Then the value in fact column will be used as variable to create scatter plot to find association between gun per capital and these fact value.
# 

# In[35]:


#Transpose Census data and remove the index on Fact
census.set_index('Fact',inplace=True)
census_T = census.T.reset_index()


# In[36]:


#Rename the column name from index to state to match the column name in gun data. 
census_T.rename(columns={'index':'state'},inplace = True)


# In[37]:


#Get subset data for 2016 and 2010
gun_16=gun[gun['year'] == 2016]
gun_10=gun[gun['year'] == 2010]


# In[38]:


#Group by gun data by state and gun totals for 2010 and 2016 
guntotal_16= gun_16.groupby(['state'])['totals'].sum().reset_index()
guntotal_10= gun_10.groupby(['state'])['totals'].sum().reset_index()


# In[39]:


#Rename the dataset to represent different time point 
guntotal_16.rename(columns={'totals':'2016_totals'},inplace = True)
guntotal_10.rename(columns={'totals':'2010_totals'},inplace = True)


# In[40]:


#Merge 2010 and 2016 gun data summary 
guntotal = guntotal_16.merge(guntotal_10, on='state', how='inner')


# In[41]:


#Merge gun and census data with inner join, by state column 
result = guntotal.merge(census_T, on='state', how='inner')


# In[42]:


#calculate Gun_Per_Capital for 2016
result['Gun_Per_Capital_2016'] = result['2016_totals']/result['Population estimates, July 1, 2016,  (V2016)']


# In[43]:


#calculate Gun_Per_Capital for 2010
result['Gun_Per_Capital_2010'] = result['2010_totals']/result['Population estimates base, April 1, 2010,  (V2016)']


# In[44]:


#Top 5  the highest state per capital on 2010
result.nlargest(5,'Gun_Per_Capital_2010')


# In[45]:


#Top 5  the highest gun per capital state on 2016
result.nlargest(5,'Gun_Per_Capital_2016')


# In[153]:


#Drop non fact value
fact = result.drop(['Gun_Per_Capital_2010','state','FIPS Code','2016_totals','2010_totals'],axis=1)


# In[79]:


#create scatter plot for all the fact variable in speparate figure by Name Group

#figure1: firms related Variable and Gun_Per_Capital 
#Use for loop to create scatter plot for  firms variable in one figure
for col in list(fact):
    if 'firms' in col:
        plt.scatter(fact[col],fact['Gun_Per_Capital_2016'], label =col)
           
plt.ylabel("Gun_Per_Capital_2016")
plt.title("figure1: firms Variable and Gun_Per_Capital Scatter Plot")
plt.grid(True)
plt.legend(bbox_to_anchor=(1.1, 1.05))
plt.show()

#figure2: Employment related Variable and Gun_Per_Capital 
#Use for loop to create scatter plot for Employment variable in one figure 
for col in list(fact):
    if 'employ' in col:
        plt.scatter(fact[col],fact['Gun_Per_Capital_2016'], label =col)
        plt.xlabel(col)
plt.ylabel("Gun_Per_Capital_2016")
plt.title("Figure4: Employee Variable and Gun_Per_Capital Scatter Plot")
plt.grid(True)
plt.legend(bbox_to_anchor=(1.1, 1.05))
plt.show()


# In[161]:


#Keep only 6 variable in fact table to create scatter plot with Gun Per capital since they have week association
imp =['White alone, percent, July 1, 2016,  (V2016)',
    'Persons 65 years and over, percent, April 1, 2010',
    'Owner-occupied housing unit rate, 2011-2015',
    'Asian alone, percent, July 1, 2016,  (V2016)',
    'Foreign born persons, percent, 2011-2015', 
    'Median gross rent, 2011-2015']


# In[168]:


#create scatter plot for all the fact variable in speparate figure, 6 figures

for col in imp:
    plt.figure(figsize=(4,4))
    print(col)
    plt.scatter(fact[col],fact['Gun_Per_Capital_2016'], label =col)
    plt.title(col+" and Gun_Per_Capital Scatter Plot")     
    plt.ylabel("Gun_Per_Capital_2016")
    plt.xlabel(col)
    plt.grid(True)
    plt.show()


# ### Research Question 2  :
# Which states have had the highest growth and the lowest growth in gun registrations? 
# 
# Alaska had the highest growth in gun registrations in Jul 2017, increasing by 403.20% compare to Apr 2010.
# Additionally,Alaska,Wyoming,Montana,Kansas,Arkansas are the top 5 state with highest growth in gun registrations in Jul 2017.Alaskas and Wyoming are only two state whose growth more than 400%
# also from the gun growth bar chart for all the states, we can see Utah and Indiana are the only two states whose gun growth are descreasing by more than 100%. On the other hand, there are 8 states' gun growth more than 300%, which can be considered outliers

# In[81]:


#Calculate the increasing percentage of gun registrations from 2010 to 2016
result['gun_growth'] = result['2016_totals']/(result['2016_totals']-result['2010_totals'])


# In[62]:


#Get the biggest growth percentage 
result['gun_growth'].max() # the result of the biggest growth perentage  is 403.20%


# In[63]:


#List Top 5 rows by gun growth rate descending
result.nlargest(5,'gun_growth')


# In[150]:


#Create Bar chart for every states'gun growth 
#Set the figure size 
plt.figure(figsize=(30,30))

plt.rcdefaults()
fig, ax = plt.subplots()

#Sort result data by gun_growth value
sorted = result.sort_values(by=['gun_growth'])

#create bar chart 
y_pos = np.arange(len(sorted['state']))
error = np.random.rand(len(sorted['state']))
ax.barh(y_pos, (sorted['gun_growth']*100), xerr=error, align='center',height=2,linewidth=5,color='green', ecolor='black')

#set x and y axis lable and make the label readable
ax.set_yticks(y_pos)
ax.set_xlabel("Gun Registration Growth %")
ax.set_yticklabels(sorted['state'],size=6)

#Invert x and y axis
ax.invert_yaxis()  # labels read top-to-bottom

#Set tick colors:
ax.tick_params(axis='x', colors='green')
ax.tick_params(axis='y', colors='black')

#Set the title
plt.title("State Gun Registration Growth from 2010 and 2016")     
plt.grid(True)
plt.legend(bbox_to_anchor=(1.1, 1.05))
plt.show()


# Findings:From the above bar chart, we can see Utah and Indiana are the only two states whose gun growth are descreasing by more than 100%. On the other hand, there are 8 states' gun growth more than 300%, which can be considered outliers.

# ### Research Question 3  :
# 
# What is the overall trend of gun purchases?
# From the line trend for gun purchases by years, we can tell that 
# from 1998 to 2016, the  overall of gun purchases is increasing. 
# From 1999 to 2005, the number of gun purchases remains stable, and from 2005 to 2016, the number of gun purchases increase from about 10 million to 2.7 million. From 2016 to 2017, the  number of gun purchases goes down, which is partially due to only 9 months in 2017 being calculated. 
# 
# From the line trend for gun purchases by months, we can see the trend of gun purchases varies month to month repeatedly within year, despite the overall upwarding trend. December and January is around the gun perchase peak every year.

# In[169]:


#Create line plot for gun purchase from 2010 to 2016 to observe the overall trend

#1. Create line chart using grouped data by year- months, which can be used to observe the change patten 
#during the season

#Assign figure size
plt.figure(figsize=(10,5))

gun.groupby('month')['totals'].sum().plot(kind='line',sharex=True, sharey=True, layout = (2, 1))
#set x and y axis lable name
plt.xlabel('Month')
plt.ylabel('Total gun purchases')
plt.legend()
plt.title("Gun Purchase Trend by months Line Chart")
plt.show()

#2. Create line chart using grouped data by year, which can be used to observe the change during the season
plt.figure(figsize=(10,6))
gun.groupby('year')['totals'].sum().plot(kind='line')

plt.ylabel('Total gun purchases')
plt.xlabel('year')
plt.title("Gun Purchase Trend by years Line Chart")
plt.legend()
plt.show()


# <a id='conclusions'></a>
# ## Conclusions

# FBI Gun and census data are two independent table. Their common variables/value include state of United States and year month, which requires data cleaning at first. We can join these two dataset to see the relationship between gun purchase and census variable.
# 
# Post Question:
# 1.What census variable or fact value is most associated with high gun per capita per state? Ceusus data includes state as variable, and there are 65 differnt census measurement as value of Fact. 
# 2.Which states have had the highest growth and the lowest growth in gun registrations from Apr 2010 to Jul 2016? 
# 3.What is the overall trend of gun purchases by year or by year and month?
# 
# Findings for the Quesitons:
# 
# 1.The gun and census data are divided by state with United state. High gun per capita should also be calculated by state, except {'District of Columbia','Guam','Mariana Islands','Puerto Rico','Virgin Islands'}. these states' gun total is missing or zero. Among all the state, Kentucky has the highest gun per capita on Jul 2016 and Apr 2010 data. Kentucky,Indiana,Illinois,West Virginia,Montana are the top 5 state who have highes gun per capita on Jul 2016.
# also, based on the scatter plot for all the fact value in one figure and group by column name scatterplot,there is no strong association between any fact value and high gun per capita.
# However, based on the scatter plot for fact varible and gun per capita, separately, there is some weak association found as following; the positive association between gun per capita and variables which includes: White alone, percent, July 1, 2016, (V2016) Persons 65 years and over, percent, April 1, 2010 owner-occupied housing unit rate, 2011 -2015
# the negative association between gun per capita and variables which includes:  2011-2015 Asian alone, percent, July 1, 2016, (V2016) Foreign born persons, percent, 2011-2015 Median gross rent, 2011-2015
# 
# 2.Alaska had the highest growth in gun registrations in Jul 2017, increasing by 403.20% compare to Apr 2010.
# Additionally,Alaska,Wyoming,Montana,Kansas,Arkansas are the top 5 state with highest growth in gun registrations in Jul 2017.Alaskas and Wyoming are only two state whose growth more than 400%
# also from the gun growth bar chart for all the states, we can see Utah and Indiana are the only two states whose gun growth are descreasing by more than 100%. On the other hand, there are 8 states' gun growth more than 300%, which can be considered outliers.
# 
# 3.From the line chart for gun purchases by years, we can tell that 
# from 1998 to 2016, the  overall of gun purchases is increasing. 
# From 1999 to 2005, the number of gun purchases remains stable, and from 2005 to 2016, the number of gun purchases increase from about 10 million to 2.7 million. From 2016 to 2017, the  number of gun purchases goes down, which is partially due to only 9 months in 2017 being calculated. 
# 
# From the line chart for gun purchases by months, we can see the trend of gun purchases varies month to month repeatedly within year, despite the overall upwarding trend. December and January is around the gun perchase peak every year.
# 
# Limitations:
# I replace gun data's missing values with mean of each columns and remove 'Fact Note' column since it has exceeding number of Nan values. Missing data can occur because of nonresponse: no information is provided.for the gun data, missing value can be caused by nonreponse or limitation regulation or lack of gathering data. My solution for replaing missing data with mean and drop null columns are not time consuming.
# 
# a. For potential improvement, in statistic, probablity distribution graphic can be used to see variable's distribution(normalized/ right-skewed/left skewed) and make prediction of missing value based on mean/ standard deviation. 
# b. Also, standardization of datasets before exploring it can help show more clear and strong correlation between variable, for example, gun per capital and Fact metrics.
# c. Additionally, the gun data contains many outliers, scaling using the mean and variance of the data is likely to not work very well. In these cases,  robust_scale and RobustScaler scaling method can be considered to remove outliers and center the data.
# 
# In result, the gun purchase has upwarding trend over last 12 years and state is most import perspective to look the gun data, some census varible has week positive and negative association with gun registration.

# In[170]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

