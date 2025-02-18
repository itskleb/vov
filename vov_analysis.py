import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title('Voice of the Volunteer')


df = pd.read_csv('Voice_of_the_Volunteer_20252025-02-18_10_17_05.csv')
df.columns = ['sub_date','motive','council_name','de_purp','camp','pain','program','length','youth','num_youth','multiple','district_vol','scout_as_youth','eagle']
df = df.fillna('No Response')


troops = df[df['program'] == 'Troop']
packs = df[df['program'] == 'Pack']
others = df[~df['program'].isin(['Pack','Troop'])]

def rankers(df,t):

  if t == 'de_purp':
    tops = ['Technical Assistance (My.Scouting guides, password assistance, reservation help, etc.)',
    'Program Delivery (Planning program, attending activities, etc.)',
    'Membership Recruitment and New Unit growth',
    'Unit issue reconciliation']
    ret_dict = dict(zip(tops,[0,0,0,0]))
  elif t == 'camp':
    tops = ['Affordability',
    'Camp Facilities',
    'Accessibility and distance from NYC',
    'Staffing Quality',
    'Program offerings']
    ret_dict = dict(zip(tops,[0,0,0,0,0]))
  else:
    tops = ['Access to the main office',
    'Access to correct staff',
    'Helpfulness of staff',
    'Cost of GNYC activities (cost of registration is controlled by national)',
    'Lack of activity calendar']
    ret_dict = dict(zip(tops,[0,0,0,0,0]))
    
  for index, row in df.iterrows():
      data = row[t].split('\n')
      for x in data:
          for y in tops:
              try:
                  s_score = int(x.split(y)[0].replace(" ",''))
                  score = ret_dict[y]+s_score
                  ret_dict.update({y:score})
                  break
              except:
                  pass
  
  return(pd.Series(ret_dict,name=t).sort_values(ascending=True))

with st.sidebar:
  prgm = st.multiselect('Program',df.program.unique().tolist(),df.program.unique().tolist())
  lgth = st.multiselect('Tenure',df.length.unique().tolist(),df.length.unique().tolist())
  youth = st.multiselect('Youth in Program',df.youth.unique().tolist(),df.youth.unique().tolist())
  dist = st.multiselect('District Volunteer',df.district_vol.unique().tolist(),df.district_vol.unique().tolist())
  eagle = st.multiselect('Eagle Scout',df.eagle.unique().tolist(),df.eagle.unique().tolist())
  scoutAsYouth = st.multiselect('Scout as Youth',df.scout_as_youth.unique().tolist(),df.scout_as_youth.unique().tolist())

#if prgm != None:
topic = st.multiselect('Select Question Topic',df.columns.tolist(),None)
temp2 = df[df['program'].isin(prgm) & df['length'].isin(lgth) & df['youth'].isin(youth) & df['district_vol'].isin(dist) & df['eagle'].isin(eagle) & df['scout_as_youth'].isin(scoutAsYouth)]
for t in topic:
  if t in ['de_purp','camp','pain']:
    st.write(f"Total Respondents: {len(temp2)}. That is {round((len(temp2)/len(df))*100,2)}% of total.")
    st.write(rankers(temp2,t))
    charty, ax = plt.subplots()
    ax.pie(rankers(temp2,t))
    st.pyplot(charty)
  else:
    temp = temp2.groupby(by=[t,'program']).count()['sub_date'].sort_values(ascending=False)
    st.write(f"Total Respondents: {len(temp2)}. That is {round((len(temp2)/len(df))*100,2)}% of total.")
    #st.write(temp.reset_index())
    chart = px.bar(temp.reset_index(),x=t,y='sub_date',title=t,labels={'sub_date':'responses'},text_auto = True,color='program')
    #chart.update_layout(showlegend=False)
    st.plotly_chart(chart)
    #st.bar_chart(data=temp,  horizontal=False)
