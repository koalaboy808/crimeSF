
# coding: utf-8

# # Loading Library

# In[2]:

# pandas
import pandas as pd

# numpy
import numpy as np

# defaultcit
from collections import defaultdict

# plot with folium
import folium
from IPython.core.display import HTML

# parsing time
from datetime import datetime, timedelta

# plotting with matplotlib
import matplotlib.pyplot as plt
import matplotlib
get_ipython().magic('matplotlib inline')

# plotting with pylab
import pylab as P

# Clustering
from sklearn.cluster import MiniBatchKMeans, KMeans
import time
import json

# change prediction categories into labels
from sklearn import preprocessing
from sklearn import cross_validation 
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor

import seaborn as sns
import re

from sklearn.naive_bayes import BernoulliNB
from sklearn.cross_validation import train_test_split
from sklearn.metrics import log_loss

from nltk import FreqDist
from xgboost import XGBClassifier


# ## Loading Training/Testing Data

# ** subset to only the fields we need and used in submission (Dates, DayOfWeek, PdDistrict, Address, X, Y, Category) **

# In[14]:

test_df = pd.read_csv("test.csv")
train_df = pd.read_csv("train.csv")
train_df = train_df.sample(n = 100000, random_state = 666)


# In[16]:

#Look at the shape
print(train_df.shape)
print(test_df.shape)


# ## Feature Creation

# ** create feature for training data and also for test data **
# 
# ** difference btw train/test is that training has category data **

# In[17]:

def createFeature(train_df):
    #Getting Month of Year, Day of Month, Hour of Day, and Minute of Hour
    month_of_year = []
    day_of_month =[]
    hour_of_day =[]
    min_of_hour =[]
    month_and_day =[]
    for i in range(len(train_df.Dates.values)):
        moy = datetime.strptime(train_df.Dates.values[i], "%Y-%m-%d %H:%M:%S").month
        dom = datetime.strptime(train_df.Dates.values[i], "%Y-%m-%d %H:%M:%S").day
        hod = datetime.strptime(train_df.Dates.values[i], "%Y-%m-%d %H:%M:%S").hour
        moh = datetime.strptime(train_df.Dates.values[i], "%Y-%m-%d %H:%M:%S").minute
        month_of_year.append(moy)
        day_of_month.append(dom)
        hour_of_day.append(hod)
        min_of_hour.append(moh)
        #month_and_day.append((moy, dom))
    train_df['month_of_year'] = month_of_year #Month of the Year feature added
    train_df['day_of_month'] = day_of_month # Day of Month feature added
    train_df['hour_of_day'] = hour_of_day # Hour of Day feature added
    train_df['min_of_hour'] = min_of_hour # Minute of Hour Feature added
#    train_df['month_and_day'] = month_and_day # Month and Date
    
    #Creating Weeekday/Weekended Feature
    train_df['WeekdayWeeekend'] = train_df['DayOfWeek'].map( {'Monday': 'Weekday', 'Tuesday': 'Weekday',                                                           'Wednesday': 'Weekday', 'Thursday': 'Weekday', 'Friday': 'Weekend',                                                         'Saturday': 'Weekend', 'Sunday': 'Weekday'} ).astype(object)
    # Creating Midnight/Morning/Afternoon/Night Column
    train_df['TimeOfDay'] = train_df['hour_of_day'].map({0: 'Midnight', 1: 'Midnight', 2:'Midnight', 3:'Midnight', 4:'Morning',                                                      5:'Morning', 6:'Morning', 7:'Morning', 8:'Morning', 9:'Morning',                                                      10:'Morning', 11:'Morning', 12:'Afternoon', 13:'Afternoon', 14:'Afternoon',                                                      15:'Afternoon', 16:'Afternoon', 17:'Afternoon', 18:'Night', 19:'Night',                                                      20:'Night', 21:'Night', 22:'Midnight', 23:'Midnight'}).astype(object)
    # Creating Season Feature
    train_df['Season'] = train_df['month_of_year'].map({1: 'Winter', 2: 'Winter', 3:'Spring', 4:'Spring', 5:'Spring',                                                      6:'Spring', 7:'Summer', 8:'Summer', 9:'Summer', 10:'Autumn',                                                      11:'Autumn', 12:'Winter'}).astype(object)

    
    train_df['District_Type'] = train_df['PdDistrict'].map({'PARK': 'Crime', 'CENTRAL': 'Other', 'MISSION': 'Crime', 'NORTHERN': 'Other', 
                                                              'TENDERLOIN': 'Crime', 'INGLESIDE': 'Crime', 'TARAVAL': 'Crime', 
                                                              'SOUTHERN': 'Crime', 'BAYVIEW': 'Crime', 'RICHMOND': 'Crime'}).astype(object)

    ###Creating feature DANGEROUS_Address
    d = {}
    address_list = []
    for address in train_df['Address']:
        address_list.append(address)
    f = FreqDist(address_list)
    common_list = f.most_common(15)
    list_d = []
    for address in common_list:
        list_d.append(address[0])
    for address in train_df['Address'][:10000]:
        if address in list_d:
            d[address] = 'Danger'
        else:
            d[address] = 'A_Other'
    train_df['Address_Type'] = train_df['Address'].map(d)
    
    ###Creating feature DANGEROUS_DATES 
    date_list = []
    i = 0
    for date in train_df['Dates']:
        while i < len(train_df.Dates.values):
            moy = datetime.strptime(train_df.Dates.values[i], "%Y-%m-%d %H:%M:%S").month
            dom = datetime.strptime(train_df.Dates.values[i], "%Y-%m-%d %H:%M:%S").day
            date_list.append(((moy, dom)))
            i += 1
    train_df['Month_Day'] = date_list
    date_f = FreqDist(date_list)
    date_common_list = date_f.most_common(30)

    list_date = []
    dateDict = {}
    for date in date_common_list:
        list_date.append(date[0])

    j = 0
    for date in train_df['Dates']:
        while j < len(train_df.Dates.values):
            moy = datetime.strptime(train_df.Dates.values[j], "%Y-%m-%d %H:%M:%S").month
            dom = datetime.strptime(train_df.Dates.values[j], "%Y-%m-%d %H:%M:%S").day
            if (moy, dom) in list_date:
                dateDict[(moy, dom)] = 'Danger_Date'
            else:
                dateDict[(moy, dom)] = 'Not_Danger_Other'
            j += 1
    train_df['Date_Type'] = train_df['Month_Day'].map(dateDict)
    
    #Deleting features not needed
#     train_df = train_df.drop('Descript', 1)
#     train_df = train_df.drop('Resolution', 1)
    #train_df = train_df.drop('Address', 1)
    
    #Creating Dummy Variables
    WeekdayWeekend_dummies = pd.get_dummies(train_df.WeekdayWeeekend)
    TimeOfDay_dummies = pd.get_dummies(train_df.TimeOfDay)
    season_dummies = pd.get_dummies(train_df.Season)
    district_dummies = pd.get_dummies(train_df.PdDistrict)
    week_dummies = pd.get_dummies(train_df.DayOfWeek)
#     type_dummies = pd.get_dummies(train_df.Crime_Type)
    corner_dummies = pd.get_dummies(train_df.District_Type)
    address_dummies = pd.get_dummies(train_df.Address_Type)
    date_dummies = pd.get_dummies(train_df.Date_Type)
    
    train_df_new = pd.concat([train_df, WeekdayWeekend_dummies, TimeOfDay_dummies, season_dummies, district_dummies, week_dummies, corner_dummies, address_dummies, date_dummies], axis=1, join_axes=[train_df.index])
    print('Sanity Check')
    print(train_df.shape)
    print(WeekdayWeekend_dummies.shape)
    print(TimeOfDay_dummies.shape)
    print(season_dummies.shape)
    print(district_dummies.shape)
    print(week_dummies.shape)
#     print(type_dummies.shape)
    print(corner_dummies.shape)
    print(address_dummies.shape)
    print(date_dummies.shape)
    print(train_df_new.shape)
    print('Make sure the total adds up to the last number')
    
    return train_df_new
    
def createCrime(train_df):
    le_crime = preprocessing.LabelEncoder()
    crime = le_crime.fit_transform(train_df.Category)
    train_df['dummy_Category'] = crime
    
    return train_df

#Calling the feature creation function
train_df_new = createCrime(createFeature(train_df))
train_df_new.head()


# In[5]:

test_df_new = createFeature(test_df)
test_df_new.head()


# In[6]:

test_df_new.shape, train_df_new.shape


# ##Prediction

# ### Feature Inclusion/Exclusion

# In[7]:

# Lat/Long
X_feature = (True, 'X')
Y_feature = (True, 'Y')

# Time
Month_feature = (True, 'month_of_year')
Day_feature = (True, 'day_of_month')
Hour_feature = (True, 'hour_of_day')
Min_feature = (True, 'min_of_hour')

# Day of Week
Friday_feature = (True, 'Friday') 
Monday_feature = (True, 'Monday')
Saturday_feature = (True, 'Saturday')
Sunday_feature = (True, 'Sunday')
Thursday_feature = (True, 'Thursday')
Tuesday_feature = (True, 'Tuesday')
Wednesday_feature = (True, 'Wednesday')

#Weekday/Weekend
Weekday_feature = (True, 'Weekday') 
Weekend_feature = (True, 'Weekend') 

#Season 
Autumn_feature = (True, 'Autumn') 
Spring_feature = (True, 'Spring') 
Summer_feature = (True, 'Summer') 
Winter_feature = (True, 'Winter') 

#Time of Day
Midnight_feature = (True, 'Midnight') 
Morning_feature = (True, 'Morning') 
Afternoon_feature = (True, 'Afternoon') 
Night_feature = (True, 'Night') 

# District
BAYV_feature = (True, 'BAYVIEW')
CENT_feature = (True, 'CENTRAL')
INGL_feature = (True, 'INGLESIDE')
MISS_feature = (True, 'MISSION')
NORT_feature = (True, 'NORTHERN')
PARK_feature = (True, 'PARK')
RICH_feature = (True, 'RICHMOND')
SOUT_feature = (True, 'SOUTHERN')
TARA_feature = (True, 'TARAVAL')
TEND_feature = (True, 'TENDERLOIN')

# # Crime Type
# Blue_feature = (False, 'Blue')
# White_feature = (False, 'White')
# Other_feature = (False, 'Other')

# District Type
# Corner_feature = (True, 'Corner')
# Street_feature = (True, 'Street')
# District_Other_feature = (True, 'Other')

# District Type Based on Crime Density by looking at Blue, White, Other
District_Other_feature = (True, 'Other')
District_Crime_feature = (True, 'Crime')

# Address Type
Address_Danger_feature = (True, 'Danger')
Address_Other_feature = (True, 'A_Other')

# Date Type
Danger_Date_feature = (True, 'Danger_Date')
Not_Danger_Date_feature = (True, 'Not_Danger_Other')


# In[8]:

feature_list = [
                X_feature, Y_feature,
                Month_feature, 
                Day_feature,
                Hour_feature, 
                Min_feature,
                #Monday_feature, Tuesday_feature, Wednesday_feature, Thursday_feature, Friday_feature, 
                Saturday_feature, Sunday_feature,
                Weekday_feature, Weekend_feature, 
                #Autumn_feature, Spring_feature, Summer_feature, Winter_feature,
                Midnight_feature, Morning_feature, Afternoon_feature, Night_feature, 
                BAYV_feature, CENT_feature, INGL_feature, MISS_feature, NORT_feature, PARK_feature, 
                RICH_feature, SOUT_feature, TARA_feature, TEND_feature,
                #Corner_feature, Street_feature, District_Other_feature,
                Address_Danger_feature, Address_Other_feature,
                Danger_Date_feature, Not_Danger_Date_feature,
                #District_Crime_feature, District_Other_feature
               ]
features = [str(x[1]) for x in feature_list if x[0]]


# # Trainding and Validation

# In[10]:

training, validation = train_test_split(train_df_new, train_size=.60)
#Score to beat 2.55250 

model = BernoulliNB()
model.fit(training[features], training['dummy_Category'])
predicted = np.array(model.predict_proba(validation[features]))
log_loss(validation['dummy_Category'], predicted)


# In[ ]:

from xgboost import XGBClassifier
model = XGBClassifier(max_depth=8,n_estimators=128)
model.fit(training[features], training['dummy_Category'])
predicted = np.array(model.predict_proba(validation[features]))
log_loss(validation['dummy_Category'], predicted)


# In[ ]:

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(max_depth=16,n_estimators=1024)
model.fit(training[features], training['dummy_Category'])
predicted = np.array(model.predict_proba(validation[features]))
log_loss(validation['dummy_Category'], predicted)


# ### Logistic Regression

# In[ ]:

#Logistic Regression for comparison
model = LogisticRegression(C=10)
model.fit(training[features], training['dummy_Category'])
predicted = np.array(model.predict_proba(validation[features]))
log_loss(validation['dummy_Category'], predicted) 


# ##Submission with XGBClassifier

# In[11]:

test_df_new = test_df_new.ix[:,1:len(test_df_new)]
test_df_new.shape


# In[12]:

#model = BernoulliNB()
model = XGBClassifier(max_depth=8,n_estimators=128)
model.fit(train_df_new[features], train_df_new['dummy_Category'])


# In[13]:

predicted = np.array(model.predict_proba(test_df_new[features]))


# In[14]:

ex_submission = pd.read_csv("sampleSubmission.csv")


# In[15]:

result= pd.DataFrame(predicted, columns=ex_submission.columns[1:len(ex_submission)])
result.to_csv('testResult2.csv', index = True, index_label = 'Id' )

