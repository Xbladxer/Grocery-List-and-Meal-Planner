import streamlit as st
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="My Plans", page_icon="📖", layout="wide")
st.title("My Plans 📖")
st.write("Here you can save and manage your favorite recipes.")

with st.container():
    col1, col2 = st.columns([2, 1])

    with col1:
        pass
    
    with col2:
        pass

if 'recipes' not in st.session_state:
    st.session_state.recipes = []
def add_recipe():
    recipe_name = st.text_input("Recipe Name", "")
    ingredients = st.text_area("Ingredients (comma-separated)", "")
    instructions = st.text_area("Instructions", "")
    
    if st.button("Add Recipe"):
        if recipe_name and ingredients and instructions:
            recipe = {
                "name": recipe_name,
                "ingredients": [ingredient.strip() for ingredient in ingredients.split(",")],
                "instructions": instructions
            }
            st.session_state.recipes.append(recipe)
            st.success(f"Recipe '{recipe_name}' added successfully!")
        else:
            st.error("Please fill in all fields.")



def display_recipes():
    if st.session_state.recipes:
        st.subheader("Saved Recipes")
        for idx, recipe in enumerate(st.session_state.recipes):
            st.write(f"**{recipe['name']}**")
            st.write("**Ingredients:** " + ", ".join(recipe['ingredients']))
            st.write("**Instructions:** " + recipe['instructions'])
            if st.button(f"Delete Recipe {idx + 1}"):
                del st.session_state.recipes[idx]
                st.success(f"Recipe '{recipe['name']}' deleted successfully!")
                break
    else:
        st.write("No recipes saved yet.")

add_recipe()
display_recipes()