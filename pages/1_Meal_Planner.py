import streamlit as st

from dotenv import load_dotenv
import os
import openai

st.set_page_config(page_title="Meal Planner", page_icon="🍽️", layout="wide")


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


#Configure Gemini
#API_KEY = os.getenv("GEMINI_API_KEY")
#genai.configure(api_key=API_KEY)
#model = genai.GenerativeModel("gemini-1.5-pro")

def plan(cal, cui, wei, age, die, res, goa, lif, no_m, no_w, no_b, no_p, pref):
    prompt = f"""
    You are a meal planner bot. Generate a meal plan, the macros, and list out the ingredients and how much of those ingredients you would need accurately based on the following parameters: {cal} for caloric intake, {cui} for cuisine preference, {wei} for body weight, {age} for age, {die} for dietary preferences, {res} for allergies or restrictions, {goa} for health goals, {lif} for lifestyle, {no_m} meals per day, {no_w} weeks of meal plan, budget of {no_b}, and serving size for {no_p} people. Based on {no_w}, write a meal plan for the given number of weeks or months. Also, return the recipe for each meal, and don't give too many meals in a single week.
    Include the macros for each meal, and ensure that the total caloric intake matches the daily caloric intake specified.
    Include any specific food preferences: {pref}.
    
    """
    
    response  = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            
            {"role": "user", "content": prompt}
        ],)
    return response.choices[0].message.content




def main():
    st.title("Meal Planner 🍽️")
    st.subheader("Create your personalized meal plan!")
    st.write("Fill out the form below to get a customized meal plan tailored to your dietary needs and preferences.")

    col1, col2, col3 = st.columns([1, 2, 1])



    with col1:
        cal = st.text_input("Daily caloric intake: ", value="", type="default")
        cui = st.text_input("Preferred cuisine:  ", value="", type="default")
        wei = st.text_input("Body weight: ", value="", type="default")
        age = st.text_input("Age: ", value="", type="default")

    with col2:
        die =st.selectbox("Dietary preferences: ",("Non-vegetarian","Vegetarian","Vegan","Keto","Pescatarian","Halal","Ethically-sourced"),placeholder= "What type of diet do you follow?")
        res = st.selectbox("Allergies/Restrictions: ",("None","Peanuts","Lactose","Soy","Gluten","Shellfish","Eggs"),placeholder= "Do you have any allergies or dietary restrictions?")
        goa = st.selectbox("Health Goals: ",("Weight loss","Maintain Weight","Weight gain"),placeholder= "Select body goal...")
        lif = st.selectbox("Lifestyle: ",("Highly active","Moderately active","Sedentary"), placeholder="How active are you?")
    with col3:
        no_m = st.select_slider("How many meals do you eat in a day?", options=("1","2","3","4","5","6","7","8","9","10"), value="3")
        no_w = st.select_slider("For how long do you need the meal plan?", options=("1 week","2 weeks","3 weeks"), value="1 week")
        no_b = st.select_slider("How much do you want to spend on groceries per week? (In rupees)", options=("Less than 1000","1000-3000","3000-6000","6000-9000","9000+"), value="1000-3000")
        no_p = st.select_slider("For how many people do you need the meal plan?", options=("1","2","3","4","5","6","7","8","9","10"), value="1")

    pref = st.text_area("Any specific food preferences: ", placeholder="Anything you'd like to mention which we haven't covered earlier", value="")
    if st.button("Generate Meal Plan", type="primary", use_container_width=True):
        with st.spinner("Generating meal plan..."):
            
            meal_plan = plan(cal, cui, wei, age, die, res, goa, lif, no_m, no_w, no_b, no_p, pref)
            generated_meal_plan = meal_plan
            st.session_state["meal_plan"] = meal_plan
            st.success("Meal plan generated successfully!")

   
            
             
            
    if "meal_plan" in st.session_state:
                st.markdown("### Your Meal Plan:")
                st.write(st.session_state["meal_plan"])

                if st.button("Save Meal Plan"):
                     if "recipes" not in st.session_state:
                          st.session_state.recipes = []
                     st.session_state.recipes.append({
                        "name": "Meal Plan",
                        "ingredients": [],
                         "instructions": st.session_state["meal_plan"]
                     })
           
    if st.button("Clear Meal Plan", type="secondary", use_container_width=True):
        if "meal_plan" in st.session_state:
            del st.session_state["meal_plan"]
            st.success("Meal plan cleared successfully!")
        else:
            st.warning("No meal plan to clear.")
    
  
if __name__ == "__main__":
    main()