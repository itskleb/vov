import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title('Voice of the Volunteer')


df = pd.read_csv('Voice_of_the_Volunteer_20252025-02-18_10_17_05.csv')
df.columns = ['sub_date','motive','council_name','de_purp','camp','pain','program','length','youth','num_youth','multiple','district_vol','scout_as_youth','eagle']

troops = df[df['program'] == 'Troop']
packs = df[df['program'] == 'Pack']
others = df[~df['program'].isin(['Pack','Troop'])]

purp = ['Technical Assistance (My.Scouting guides, password assistance, reservation help, etc.)',
'Program Delivery (Planning program, attending activities, etc.)',
'Membership Recruitment and New Unit growth',
'Unit issue reconciliation']

camp = ['Affordability',
'Camp Facilities',
'Accessibility and distance from NYC',
'Staffing Quality',
'Program offerings']

issue = ['Access to the main office',
'Access to correct staff',
'Helpfulness of staff',
'Cost of GNYC activities (cost of registration is controlled by national)',
'Lack of activity calendar']

with st.sidebar:
  prgm = st.multiselect('Program',df.program.unique().tolist(),df.program.unique().tolist())
  lgth = st.multiselect('Tenure',df.length.unique().tolist(),df.length.unique().tolist())
  youth = st.multiselect('Youth in Program',['YES','NO',np.nan],['YES','NO',np.nan])
  dist = st.multiselect('District Volunteer',df.district_vol.unique().tolist(),df.district_vol.unique().tolist())
  eagle = st.multiselect('Eagle Scout',df.eagle.unique().tolist(),None)
  scoutAsYouth = st.multiselect('Scout as Youth',df.scout_as_youth.unique().tolist(),None)

#if prgm != None:
topic = st.multiselect('Select Question Topic',df.columns.tolist(),None)
for i in topic:
  temp = df[df['program'].isin(prgm) & df['length'].isin(lgth) & df['youth'].isin(youth) & df['district_vol'].isin(dist) & df['eagle'].isin(eagle)].groupby(by=i).count()['sub_date']

  st.bar_chart(data=temp)
