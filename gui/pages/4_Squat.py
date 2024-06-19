import streamlit as st
from model import squats
from model import squat_counter
import mysql.connector
from model import squat_accuracy
from statistics import mean
from datetime import date
todays_date = date.today()


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
                f'<div class="exercise-section">Squat is an excellent exercise for building leg strength, targeting the quadriceps, hamstrings, and glutes.</div>',
            unsafe_allow_html = True)
st.sidebar.write("**Step 1: Stand Tall**\n 1. Stand with your feet shoulder-width apart, toes pointed slightly outward.")
st.sidebar.write("**Step 2: Lowering**")
st.sidebar.write("2. Push your hips back and bend your knees, lowering your body as if sitting into a chair.")
st.sidebar.write("**Step 3: Depth**")
st.sidebar.write("3. Go as low as your mobility allows, ideally until your thighs are at least parallel to the ground.")
st.sidebar.write("**Step 4: Rising**")
st.sidebar.write("4. Push through your heels and straighten your legs to return to the starting position.")

st.title("Squat 🏋️‍♂️")
st.write("Squats are the key to strong legs and a firm lower body.")
if st.button("Start"):
    squats()

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
  query = "insert into squats (date, sets, reps, accuracy) values (%s, %s, %s, %s)"
  values = (todays_date, new_sets, reps, accuracy)
  cursor.execute(query, values)
  dataBase.commit()
  cursor.close()
  dataBase.close()


 def check_db(reps):
  accuracy = round(mean(squat_accuracy), 2)
  dataBase = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "ai_gym"
  )
  curr = dataBase.cursor()
  query = "select * from squats order by squats_id desc limit 1"
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
 check_db(squat_counter[0])