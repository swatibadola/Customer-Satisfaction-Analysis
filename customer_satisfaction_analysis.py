# -*- coding: utf-8 -*-
"""Customer Satisfaction Analysis

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/172udZDM0EgXM1GcAuFanIZwox5LovRv1
"""

import pandas as pd
try:
  data = pd.read_csv('Ecommerce_data.csv')
  # ERROR HANDLING
except FileNotFoundError:
  print('Error: File not found.')
data.head()

data.columns

data.describe()

"""#### All given amounts are in $"""

import matplotlib.pyplot as plt

numeric_cols = ['Age', 'PurchaseAmount', 'PurchaseFrequency', 'ProductQualityRating', 'DeliveryTimeRating', 'CustomerServiceRating', 'WebsiteEaseOfUseRating', 'ReturnRate', 'DiscountUsage']
plt.figure(figsize=(15,20))

for i, col in enumerate(numeric_cols, 1):
  plt.subplot(5,2,i)
  # creating subplot in 5*2 grid, ith subplot selected for plotting.
  # Can have upto 10 subplots in single figure.
  plt.hist(data[col], bins=20, edgecolor='k', alpha=0.7)
  # edgecolor='k' -> setting edge color of the bins to black
  # alpha=0.7 => setting transparency level of bars
  plt.title(f'Distribution of {col}')
  # f => f-string, way to format strings in python.
  plt.xlabel(col)
  plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

"""# Segmenting customers based on demographic and behavioural factors"""

# creating age groups
bins = [18,30,40,50,60,70]
labels=['18-19','30-39','40-49','50-59','60-69']
data['AgeGroup'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)

# selecting only numeric cols
numeric_cols = ['ProductQualityRating', 'DeliveryTimeRating', 'CustomerServiceRating', 'WebsiteEaseOfUseRating']

# calculating mean ratings by age group and gender
mean_ratings_age_gender = data.groupby(['AgeGroup', 'Gender'])[numeric_cols].mean()

# reset index to display the dataframe
mean_ratings_age_gender.reset_index(inplace=True)
mean_ratings_age_gender

"""# Analyzing impact of loyalty program membership"""

numeric_cols=['ProductQualityRating', 'DeliveryTimeRating', 'CustomerServiceRating', 'WebsiteEaseOfUseRating', 'ReturnRate', 'DiscountUsage']

# calc mean ratings by loyalty program membership
mean_ratings_loyalty = data.groupby('LoyaltyProgramMember')[numeric_cols].mean()

# reset index
mean_ratings_loyalty.reset_index(inplace=True)
mean_ratings_loyalty

"""# Calculating the net promoter score (NPS).
### NPS => used to gauge customer loyalty and satisfaction asking customeres how likely do they recommend using company's product or services on a scale of 0 to 10.
### Respondents classifies in 3 categories:
1) Detractors (0-6)
2) Passives (7-8)
3) Promoters (9-10)
### How to calc?
### NPS = % of promoters - % of detractors
### Higher NPS indicates more loyalty. Play vital role for business growth
"""

# defining categories for NPS based on CustomerServiceRating
data['NPS_Category'] = pd.cut(data['CustomerServiceRating'], bins=[0, 6, 8, 10], labels=['Detractors', 'Passive', 'Promoters'], right=False)

# calc NPS
nps_counts = data['NPS_Category'].value_counts(normalize=True)*100
nps_score = nps_counts['Promoters'] - nps_counts['Detractors']

data['NPS_Category']
nps_score

"""### **CONCLUSION**: The NPS Score reveals that the 100% customers fall in the detractors list. Which leads to high customer dissatisfaction.
### **REMEDY TO IMPROVE CUSTOMER SATISFACTION** : Improve customer services

# Performing Root Cause Analysis for Customer Dissatisfaction
### Analyzing charachteristics of customers providing the low rating. Pattern recognition
### HOW? => Creating subsets of data, where ratings are low for all labels.
"""

data.columns

# defining low threshold
low_rating_threshold = 2

# creating subsets for low ratings for all the labels
low_product_quality = data[data['ProductQualityRating'] <= low_rating_threshold]
low_delivery_time = data[data['DeliveryTimeRating'] <= low_rating_threshold]
low_customer_service = data[data['CustomerServiceRating'] <= low_rating_threshold]
low_website_ease_of_use = data[data['WebsiteEaseOfUseRating'] <= low_rating_threshold]

# plotting figures for all the subsets
plt.figure(figsize=(12, 10))

# Age distribution for low ratings
plt.subplot(2,2,1)
plt.hist([low_product_quality['Age'], low_delivery_time['Age'], low_customer_service['Age'], low_website_ease_of_use['Age']], bins=10, label=['Product quality', 'Delivery time', 'Customer service', 'Website ease of use'])
plt.title('Age Distribution for low ratings')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.legend()

# Purchase amount distribution for low ratings
plt.subplot(2,2,2)
plt.hist([low_product_quality['PurchaseAmount'], low_delivery_time['PurchaseAmount'], low_customer_service['PurchaseAmount'], low_website_ease_of_use['PurchaseAmount']], bins=10, label=['Product quality', 'Delivery time', 'Customer service', 'Website ease of use'])
plt.title('Purchase amount Distribution for low ratings')
plt.xlabel('Purchase amount')
plt.ylabel('Frequency')
plt.legend()

# Age distribution for low ratings
plt.subplot(2,2,3)
plt.hist([low_product_quality['PurchaseFrequency'], low_delivery_time['PurchaseFrequency'], low_customer_service['PurchaseFrequency'], low_website_ease_of_use['PurchaseFrequency']], bins=10, label=['Product quality', 'Delivery time', 'Customer service', 'Website ease of use'])
plt.title('PurchaseFrequency Distribution for low ratings')
plt.xlabel('PurchaseFrequency')
plt.ylabel('Frequency')
plt.legend()

# Age distribution for low ratings
plt.subplot(2,2,4)
plt.hist([low_product_quality['ReturnRate'], low_delivery_time['ReturnRate'], low_customer_service['ReturnRate'], low_website_ease_of_use['ReturnRate']], bins=10, label=['Product quality', 'Delivery time', 'Customer service', 'Website ease of use'])
plt.title('ReturnRate Distribution for low ratings')
plt.xlabel('ReturnRate')
plt.ylabel('Frequency')
plt.legend()

plt.tight_layout()
plt.show()

"""### **CONCLUSION** :
### 1) High low rates in age range between 30-40 and 50-60, suggesting age related dissatisfaction.
### 2) From the purchase amount distribution, low ratings is not limited to low-spenders or infrequent buyers. High spenders and frequent buyers express dissatisfaction.
### 3) Return rate distribution is affected due to the dissatisfaction specifically related to the website ease of use and product quality.
"""