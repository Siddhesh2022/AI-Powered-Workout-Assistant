
import streamlit as st
import pandas as pd
import mysql.connector
import numpy as np
from statistics import mean
from datetime import date
todays_date = date.today()

st.title('Greetings user, your exercise report is as follows:')


exercise_data = {
 'Exercise': ['DeadLift', 'Push-Ups', 'Squats', 'Bicep Curl'],
 'Sets': [0, 0, 0, 0],
 'Reps': [0, 0, 0, 0],
 'Accuracy': [0, 0, 0, 0],
 
}

exercise_sets_reps_data = {
 'DeadLift_sets': [],
 'DeadLift_reps': [],
 'DeadLift_accuracy': [],
 'Pushups_sets': [],
 'Pushups_reps': [],
 'Pushups_accuracy': [],
 'Squats_sets': [],
 'Squats_reps': [],
 'Squats_accuracy': [],
 'Bicep_Curl_sets': [],
 'Bicep_Curl_reps': [],
 'Bicep_Curl_accuracy': [],
 
}

for key in exercise_sets_reps_data:
    exercise_sets_reps_data[key].clear()

db_exercise = ['deadlift', 'pushups', 'squats', 'bicep']
db = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "ai_gym"
  )
cursor = db.cursor()
x = 0
for i in db_exercise:
 table = i
 query = "select sets, reps, accuracy from {} where date = %s;".format(table)
 date = (todays_date,)
 cursor.execute(query, date)
 results = cursor.fetchall()
 print(results)
 if results != []:
  print(x)
  exercise_data['Sets'][x] = results[-1][0]
  exercise_data['Reps'][x] = sum(data[1] for data in results)
  exercise_data['Accuracy'][x] = (round(mean(data[2] for data in results), 2)) * 100
  if table == 'deadlift':
   for data in results:
    exercise_sets_reps_data['DeadLift_sets'].append(data[0])
    exercise_sets_reps_data['DeadLift_reps'].append(data[1])
    exercise_sets_reps_data['DeadLift_accuracy'].append(round(data[2], 2) * 100)
 
  if table == 'pushups':
   for data in results:
    exercise_sets_reps_data['Pushups_sets'].append(data[0])
    exercise_sets_reps_data['Pushups_reps'].append(data[1])
    exercise_sets_reps_data['Pushups_accuracy'].append(round(data[2], 2) * 100)
 
  if table == 'squats':
   for data in results:
    exercise_sets_reps_data['Squats_sets'].append(data[0])
    exercise_sets_reps_data['Squats_reps'].append(data[1])
    exercise_sets_reps_data['Squats_accuracy'].append(round(data[2], 2) * 100)
 
  if table == 'bicep':
   for data in results:
    exercise_sets_reps_data['Bicep_Curl_sets'].append(data[0])
    exercise_sets_reps_data['Bicep_Curl_reps'].append(data[1])
    exercise_sets_reps_data['Bicep_Curl_accuracy'].append(round(data[2], 2) * 100)
 
 x += 1

 
df = pd.DataFrame(exercise_data)
st.table(df)
st.line_chart(
 exercise_data, x = 'Exercise', y = ['Sets', 'Reps', 'Accuracy'], color= None
)



max_length = max(len(lst) for lst in exercise_sets_reps_data.values())
for key in exercise_sets_reps_data:
    exercise_sets_reps_data[key] += [None] * (max_length - len(exercise_sets_reps_data[key]))
    
sets_reps_df = pd.DataFrame(exercise_sets_reps_data)

# st.table(sets_reps_df)

option = st.selectbox(
   "Select an Exercise",
   ("DeadLift", "Push-Ups", "Bicep Curl", "Squats"),
   index=None,
   placeholder="Select an Exercise",
)

if option == "DeadLift":
 st.table(sets_reps_df[['DeadLift_sets', 'DeadLift_reps', 'DeadLift_accuracy']])
 st.bar_chart(
  sets_reps_df, x = 'DeadLift_sets', y = ['DeadLift_reps', 'DeadLift_accuracy'], color = ["#FF0000", "#0000FF"]
 )
 st.write('## Suggestions:')
 st.markdown('[Watch Deadlift Video](https://youtube.com/shorts/vfKwjT5-86k?si=bGYR3mfBwRCfjchl)')
 
if option == "Push-Ups":
 st.table(sets_reps_df[['Pushups_sets', 'Pushups_reps', 'Pushups_accuracy']])
 st.bar_chart(
  sets_reps_df, x = 'Pushups_sets', y = ['Pushups_reps', 'Pushups_accuracy'], color = ["#FF0000", "#0000FF"]
 )
 st.write('## Suggestions:')
 st.markdown('[Watch Pushups Video](https://youtube.com/shorts/SLOkdLLWj8A?si=zKCsUPmwXdiVHIu1)')

if option == "Bicep Curl":
 st.table(sets_reps_df[['Bicep_Curl_sets', 'Bicep_Curl_reps', 'Bicep_Curl_accuracy']])
 st.bar_chart(
  sets_reps_df, x = 'Bicep_Curl_sets', y = ['Bicep_Curl_reps', 'Bicep_Curl_accuracy'], color = ["#FF0000", "#0000FF"]
 )
 st.write('## Suggestions:')
 st.markdown('[Watch Bicep Curl Video](https://youtube.com/shorts/JarZJ-Wuw0g?si=dngc-r_d5rvkDilY)')

if option == "Squats":
 st.table(sets_reps_df[['Squats_sets', 'Squats_reps', 'Squats_accuracy']])
 st.bar_chart(
  sets_reps_df, x = 'Squats_sets', y = ['Squats_reps', 'Squats_accuracy'], color = ["#FF0000", "#0000FF"]
 )
 st.write('## Suggestions:')
 st.markdown('[Watch Squat Video](https://youtube.com/shorts/SLOkdLLWj8A?si=zKCsUPmwXdiVHIu1)')

 