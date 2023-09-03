## Importing Libraries
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError
###############################################################
streamlit.title("My Parent's New Healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣 Omega 3 and Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach and Rocket Smoothie")
streamlit.text("🐔 Hard/Soft-Boiled Free Range Chicken Eggs")
streamlit.text("🥑🍞 Avacado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


## create a function to get fruityvice dataframe
def get_fruityvice_data(fruit_choice):
    #Display Fruityvice api response based on user Input
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice.title() )
    # show json data in tabular form
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

##create pd dataframe to read CSV file from that S3 bucket
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include
#Also set up example of fruits in the multiselect search bar
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
options = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index), [0,1])
fruits_to_show = my_fruit_list.loc[options]

streamlit.dataframe(fruits_to_show) ##display the table on the page
try:
    ## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Fruit selected does not exist')
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
streamlit.header('FruityVice Fruit Advice')

##Check SF connection with streamlit
##snowflake related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute('SELECT * from fruit_load_list')
        return my_cur.fetchall()

##Add a button
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)


##Don't run anything from here on
#streamlit.stop()
## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
def insert_row_sf(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values('"+ new_fruit +"')")
        return "Thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input('What fruit would you like to add?','Kiwi')
if streamlit.button('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_sf(add_my_fruit)
    streamlit.text(back_from_function)

#streamlit.write('Your choice of fruit ', add_my_fruit,' is added!')

## insert rows into SF table
