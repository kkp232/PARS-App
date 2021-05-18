# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!

#---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit
# To run from terminal: streamlit run myapp.py

#---------------------------------#
# Imports
import streamlit as st
from PIL import Image
import pandas as pd
import json
import numpy as np

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")

#---------------------------------#
# Title
image = Image.open('logo.jpg')
st.image(image, width = 500)
st.title('Risk Score')
st.markdown("""
**Description:** Maximum score of 100 points.
""")

#---------------------------------#
# About
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
""")

#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.beta_columns((2,1))

#---------------------------------#
# Sidebar + Main panel
col1.header('Variables')

#---------------------------------#
# Sidebar - Predictors Input
age = col1.slider('Age (years)', 65, 85, 65)
height = col1.slider('Height (inches)', 36, 96, 36)
weight = col1.slider('Weight (lbs)', 51, 350, 51)
bmi = 703*float(weight)/float(height)**2

check_adl = col1.checkbox('ADL Score is Known')
if check_adl:
    adl = col1.slider('ADL Score (Select -1 if unknown)', -1, 100, -1)
else:
    adl = -1

check_fr = col1.checkbox('Free Recall Score is Known')
if check_fr:
    fr = col1.slider('Free Recall Score (Select -1 if unknown)', -1, 100, -1)
else:
    fr = -1


check_apo = col1.checkbox('# of e4 alleles is Known')
if check_apo:
    apoe4 = col1.radio('APOE4 (# of e4 alleles)', ['0','1','2'])
    famhist = 'Unknown'
else:
    #col2.write('INCOMPLETE: If APOE4 status is unknown then Family History is required')
    apoe4 = 'Unknown'
    famhist = col1.radio('# of Parents with Dementia', ['0','1','2'])
    #check_fh = col1.checkbox('# of Parents with Dementia is Known')
    #if check_fh:
    #    famhist = col1.radio('# of Parents with Dementia', ['0','1','2'])
    #else:
    #    famhist = 'Unknown'


#famhist = col1.selectbox('# of Parents with Dementia', ['Unknown','0','1','2'])
#apoe4 = col1.selectbox('APOE4 (# of e4 alleles)', ['Unknown','0','1','2'])

#---------------------------------#
# Page contents
col2.subheader('Risk Score')

#---------------------------------#
# Indicator vectors for age, bmi, family history, free recall, and ADL
a = float(age)
if a < 70:
    A = [1,0,0,0]
elif a < 75:
    A = [0,1,0,0]
elif a < 80:
    A = [0,0,1,0]
else:
    A = [0,0,0,1]

if bmi < 25:
    B = [1,0,0]
elif bmi < 30:
    B = [0,1,0]
else:
    B = [0,0,1]

if famhist in ['0','1','2']:
    fh = float(famhist)
    if fh==0:
        FH = [1,0,0]
    elif fh==1:
        FH = [0,1,0]
    elif fh==2:
        FH = [0,0,1]
else:
    FH = [0,0,0]
    #if apoe4 not in ['0','1','2']:
        #col2.write('INCOMPLETE: If APOE4 status is unknown then Family History is required')

f = float(fr)
if f < 20:
    FR = [1,0,0,0]
elif f < 25:
    FR = [0,1,0,0]
elif f < 31:
    FR = [0,0,1,0]
else:
    FR = [0,0,0,1]

ad = float(adl)
if ad < 64:
    AD = [1,0]
else:
    AD = [0,1]

if apoe4 in ['0','1','2']:
    ap = float(apoe4)
    if ap==0:
        APO = [1,0,0]
    elif ap==1:
        APO = [0,1,0]
    elif ap==2:
        APO = [0,0,1]
else:
    APO = [0,0,0]
    #col2.write('INCOMPLETE: If APOE4 status is unknown then Family History is required')

#---------------------------------#
# Initialize points vectors to zeros
age_points = [0,0,0,0]
bmi_points = [0,0,0]
fr_points = [0,0,0,0]
apo_points = [0,0,0]
fh_points = [0,0,0]
adl_points = [0,0]

#---------------------------------#
# Determine model and assign points
if apoe4 in ['0','1','2']:
    # Model 4
    model = 'Model 4 chosen with variables: Age, BMI, and APOE4 status.'
    age_points = [0,10,20,22]
    bmi_points = [5,0,2]
    apo_points = [0,39,73]
elif fr > -0.5:
    # Model 3
    model = 'Model 3 chosen with variables: Age, BMI, Family History, and Free Recall.'
    age_points = [0,13,26,31]
    bmi_points = [5,0,1]
    fh_points = [0,14,38]
    fr_points = [26,22,10,0]
elif adl > -0.5:
    # Model 2
    model = 'Model 2 chosen with variables: Age, BMI, Family History, and ADL Score.'
    age_points = [0,17,33,38]
    bmi_points = [5,0,1]
    fh_points = [0,17,43]
    adl_points = [14,0]
else:
    # Model 1
    model = 'Model 1 chosen with variables: Age, BMI, and Family History.'
    age_points = [0,18,40,47]
    bmi_points = [5,0,1]
    fh_points = [0,18,48]

#---------------------------------#
# Calculate score as sum of dot products between vectors
score = np.dot(A, age_points)
score = score + np.dot(B, bmi_points)
score = score + np.dot(FH, fh_points)
score = score + np.dot(APO, apo_points)
score = score + np.dot(FR, fr_points)
score = score + np.dot(AD, adl_points)

#---------------------------------#
#Output to screen
col2.write(model)
col2.write('Risk Score points total: ' + str(score))
col2.write('For educational purposes only')
col2.write('For details see: PAPER')
