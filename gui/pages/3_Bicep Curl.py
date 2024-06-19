import streamlit as st
from bicep import bicep
import mysql.connector
from datetime import date
todays_date = date.today()
from bicep import bicep_counter



st.sidebar.markdown(
        """
        <style>
            .exercise-section {
                background-color: #000000;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            }
        </style>
        """,
        unsafe_allow_html=True
    )


st.sidebar.markdown(
  f'<div class="exercise-section">Bicep Curl is a fantastic exercise for strengthening your biceps and improving upper arm strength.</div>',
  unsafe_allow_html = True)
st.sidebar.write("**Step 1: Starting Position**")
st.sidebar.write(
  "1. Stand with feet shoulder-width apart, holding dumbbells in each hand, arms fully extended, and palms facing forward.")
st.sidebar.write("**Step 2: Curl**")
st.sidebar.write(
  "2. Keeping your upper arms stationary, exhale and curl the weights while contracting your biceps.\n3. Continue until the dumbbells are at shoulder level.")
st.sidebar.write("**Step 3: Lowering**")
st.sidebar.write("4. Inhale and slowly begin to lower the dumbbells back to the starting position.")

st.title("Bicep Curls 💪")
st.write("Bicep Curls help sculpt and strengthen your arm muscles.")
if st.button("Start"):
 bicep()

if (st.button("Save Data for Analysis")):
 # st.write(counter[0])
 def add(new_sets, reps, accuracy):
  dataBase = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "ai_gym"
  )
  cursor = dataBase.cursor()
  query = "insert into bicep (date, sets, reps, accuracy) values (%s, %s, %s, %s)"
  values = (todays_date, new_sets, reps, accuracy)
  cursor.execute(query, values)
  dataBase.commit()
  cursor.close()
  dataBase.close()
 
 
 def check_db(reps):
  accuracy = 0
  dataBase = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "ai_gym"
  )
  curr = dataBase.cursor()
  query = "select * from bicep order by bicep_id desc limit 1"
  curr.execute(query)
  results = curr.fetchall()
  print(results)
  print(results[0][1])
  database_date = results[0][1]
  if todays_date == database_date:
   new_sets = (results[0][2]) + 1
   print(new_sets)
   add(new_sets, reps, accuracy)
  else:
   new_sets = 1
   add(new_sets, reps, accuracy)
 
 
 check_db(bicep_counter[0])
 