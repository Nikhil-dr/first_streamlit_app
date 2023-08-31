## Importing Libraries
import streamlit
import pandas as pd
import requests
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

#Display Fruityvice api response

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())

# show json data in tabular form
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

streamlit.dataframe(fruityvice_normalized)
