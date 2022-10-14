from urllib.error import URLError

import pandas as pd
import requests
import snowflake.connector
import streamlit

streamlit.title("My Parents New Healthy Dinner")

streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smootie")
streamlit.text("🐔 Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header("🍌🥭 Build Your Own Fruit Smoothie 🥝🍇")

my_fruit_list = pd.read_csv(
    "https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt"
)
my_fruit_list = my_fruit_list.set_index("Fruit")

fruits_selected = streamlit.multiselect(
    "Pick some fruits:", list(my_fruit_list.index), ["Avocado", "Strawberries"]
)
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


def get_fruityvice_data(this_fruit_choice):
    streamlit.write("The user entered", fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input(
        "What fruit would you like information about?", "Kiwi"
    )
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:

        fruityvice_response = requests.get(
            f"https://fruityvice.com/api/fruit/{fruit_choice}"
        )
        fruit_normalized = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruit_normalized)

except URLError as e:
    streamlit.error(e)

streamlit.header("View Our Fruit List - Add Your Favorites")


def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()


if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(
            f"insert into fruit_load_list values ('{add_my_fruit}')"
        )
        return f"thanks for adding {add_my_fruit}"


add_my_fruit = streamlit.text_input(
    "What fruit would you like to add?", "jackfruit"
)

if streamlit.button("Add a Fruit to the list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    insert_row = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(insert_row)
