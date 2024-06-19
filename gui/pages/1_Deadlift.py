import streamlit as st
from model import deadlift
from model import deadlift_counter
from model import deadlift_accuracy
import mysql.connector
from datetime import date
todays_date = date.today()
from statistics import mean


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


st.title("Deadlift 🏋️‍♂️")
st.write("Deadlift is a great exercise for building strength in your lower back, glutes, and hamstrings.")
st.sidebar.markdown(
 f'<div class="exercise-section">Deadlift is a great exercise for building strength.</div>',
 unsafe_allow_html = True)

st.sidebar.write("")
st.sidebar.write("\nHere are some tips for performing the Deadlift:")
st.sidebar.write(
 "**Step 1: Set Up**.\n1. Stand on your feet shoulder-width apart, toes pointing forward.\n2. The barbell should be over the middle of your feet.")
st.sidebar.write("**Step 2: Grip**")
st.sidebar.write(
 "3. Bend at the hips and knees to grasp the barbell with an overhand grip (palms facing you) or mixed grip (one palm facing you, one away).")
st.sidebar.write("**Step 3: Stance**")
st.sidebar.write(
 "4. Your hands should be just outside your knees.\n5. Keep your back straight, chest up, and shoulders back.")
st.sidebar.write("**Step 5: Lowering**")
st.sidebar.write(
 "9. Reverse the movement, pushing your hips back first.\n10. Lower the barbell with control, keeping it close to your body.")


if (st.button("Start")):
 deadlift()


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
  query = "insert into deadlift (date, sets, reps, accuracy) values (%s, %s, %s, %s)"
  values = (todays_date, new_sets, reps, accuracy)
  cursor.execute(query, values)
  dataBase.commit()
  cursor.close()
  dataBase.close()


 def check_db(reps):
  accuracy = round(mean(deadlift_accuracy), 2)
  dataBase = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "ai_gym"
  )
  curr = dataBase.cursor()
  query = "select * from deadlift order by deadlift_id desc limit 1"
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
 check_db(deadlift_counter[0])
 


