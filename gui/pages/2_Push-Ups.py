import streamlit as st
from model import pushup2
import mysql.connector
from datetime import date
todays_date = date.today()
from model import pushup_counter
from model import pushup_accuracy
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

st.sidebar.markdown(
    f'<div class="exercise-section">Push-ups are a versatile exercise that targets multiple muscle groups, including the chest, shoulders, and triceps.</div>',
    unsafe_allow_html = True)
st.sidebar.write("\nHere are some tips for performing the Push-Ups:")
st.sidebar.write("Step 1: Starting Position")
st.sidebar.write("1. Begin in a plank position, hands shoulder-width apart, arms fully extended, and body straight from head to heels.")
st.sidebar.write("**Step 2: Descent**")
st.sidebar.write("2. Lower your body by bending your elbows, keeping them close to your sides.\n3. Lower until your chest nearly touches the ground, or as far as your strength allows.")
st.sidebar.write("**Step 3: Pushing Up**")
st.sidebar.write("4. Push through your palms to straighten your arms, returning to the starting position.")


st.title("Push-Ups 🧎")
st.write("Push-ups are a classic bodyweight exercise that target your chest, shoulders, and triceps.")
if st.button("Start"):
 pushup2()
 
if st.button("Save Data for Analysis"):

 def add(new_sets, reps, accuracy):
  dataBase = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "ai_gym"
  )
  cursor = dataBase.cursor()
  query = "insert into pushups (date, sets, reps, accuracy) values (%s, %s, %s, %s)"
  values = (todays_date, new_sets, reps, accuracy)
  cursor.execute(query, values)
  dataBase.commit()
  cursor.close()
  dataBase.close()


 def check_db(reps):
  accuracy = round(mean(pushup_accuracy), 2)
  dataBase = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "",
   database = "ai_gym"
  )
  curr = dataBase.cursor()
  query = "select * from pushups order by pushups_id desc limit 1"
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
 check_db(pushup_counter[0])