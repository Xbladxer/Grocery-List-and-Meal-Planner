import streamlit as st
import openai
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Grocery List Generator", page_icon="🛒", layout="wide")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.header("Grocery List Generator 🛒")
st.subheader("Create your personalized grocery list!")
st.write("Fill out the form below to get a customized grocery list tailored to your dietary needs and preferences.")

meal_plan = st.session_state.get('meal_plan', None)

def extract_ingredients(meal_plan):
    prompt = f"""
    You are a grocery list generator bot. Based on the following meal plan, generate a grocery list with all the ingredients needed to prepare the meals. 
For each ingredient, list the quantity and the unit as it would be purchased in a typical grocery store (e.g., 1 dozen eggs, 1 loaf of bread, 500g pack of pasta, 1 bottle of oil, 100gm of chilli powder), not just the amount used in cooking, and display these units in metric system of measurement. Make it so that the list is easy to read and understand, with each ingredient on a new line.
Group similar items together, and ensure the list is clear and organized into different sections like Proteins, vegetables, etc., and add ~ around the section headers for emphasis.
The meal plan is as follows: {st.session_state.get("meal_plan", "No meal plan found.")}
Ensure that the quantities are accurate and suitable for the number of people and duration specified in the meal plan.
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    # Safely evaluate the list (if you trust the model output)
    try:
        ingredients = eval(response.choices[0].message.content)
    except Exception:
        ingredients = response.choices[0].message.content.splitlines()
    return ingredients

if meal_plan:
    st.write("Here is your grocery list based on the meal plan:")
    ingredients = extract_ingredients(meal_plan)

    
    
    for idx, item in enumerate(ingredients):
        line = item.strip()
        if line.startswith("~") and line.endswith("~"):
            st.markdown(f"**{line.strip('~').strip()}**")
        elif line:
            st.checkbox(item, key=f"ingredient_{idx}")
    
    st.success("Grocery list generated successfully!")
else:
    st.info("No meal plan found. Please generate a meal plan first.")