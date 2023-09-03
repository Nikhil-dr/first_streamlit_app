## Importing Libraries
import streamlit
import pandas as pd
import requests
import snowflake.connector
###############################################################
streamlit.title("My Parent's New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach and Rocket Smoothie")
streamlit.text("🐔 Hard/Soft-Boiled Free Range Chicken Eggs")
streamlit.text("🥑🍞 Avacado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

##create pd dataframe to read CSV file from that S3 bucket
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include
#Also set up example of fruits in the multiselect search bar
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
options = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index), [0,1])
fruits_to_show = my_fruit_list.loc[options]

streamlit.dataframe(fruits_to_show) ##display the table on the page
streamlit.header('FruityVice Fruit Advice')

## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#Display Fruityvice api response based on user Input

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice.title() )
#streamlit.text(fruityvice_response.json())

# show json data in tabular form
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

streamlit.dataframe(fruityvice_normalized)

##Check SF connection with streamlit
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)
