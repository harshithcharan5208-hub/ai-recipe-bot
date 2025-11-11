import streamlit as st
from openai import OpenAI
import json

st.set_page_config(
    page_title="AI Recipe Suggestion Bot",
    page_icon="🍳",
    layout="wide"
)

# Add your OpenAI API key here
OPENAI_API_KEY = "your_openai_api_key_here"

if not OPENAI_API_KEY:
    st.error("⚠️ OPENAI_API_KEY not found! Please add your API key in the code.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

st.title("🍳 AI Recipe Suggestion Bot")

st.markdown("### Get personalized recipe suggestions based on your ingredients, dietary preferences, and cuisine choices!")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🥗 Your Ingredients")
    ingredients = st.text_area(
        "Enter ingredients you have (one per line or comma-separated):",
        placeholder="e.g., chicken, tomatoes, garlic, rice",
        height=150
    )
    st.subheader("🌍 Cuisine Type")
    cuisine_options = [
        "Any", "Italian", "Indian", "Mexican", "Chinese", "Japanese", "Thai", "American",
        "French", "Mediterranean", "Korean", "Spanish", "Middle Eastern", "Greek"
    ]
    cuisine = st.selectbox("Select preferred cuisine:", cuisine_options)

with col2:
    st.subheader("🥑 Dietary Preferences")
    dietary_preferences = st.multiselect(
        "Select any dietary restrictions or preferences:",
        [
            "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Keto", "Low-Carb",
            "High-Protein", "Paleo", "Nut-Free", "Halal", "Kosher"
        ]
    )
    st.subheader("⚙️ Additional Options")
    cooking_time = st.slider("Maximum cooking time (minutes):", 15, 180, 60, 15)
    servings = st.number_input("Number of servings:", min_value=1, max_value=12, value=4)

st.markdown("---")

col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    generate_button = st.button("🔍 Get Recipe Suggestions", type="primary", use_container_width=True)
with col_btn2:
    if st.button("🔄 Clear All", use_container_width=True):
        st.experimental_rerun()

def generate_recipe(ingredients_list, dietary_prefs, cuisine_type, max_time, num_servings):
    dietary_text = ", ".join(dietary_prefs) if dietary_prefs else "No specific dietary restrictions"
    cuisine_text = cuisine_type if cuisine_type != "Any" else "any cuisine"
    prompt = f"""
You are a professional chef and recipe creator. Generate a detailed, creative recipe based on the following criteria:
Ingredients available: {ingredients_list}
Dietary preferences: {dietary_text}
Cuisine type: {cuisine_text}
Maximum cooking time: {max_time} minutes
Number of servings: {num_servings}

Please provide a complete recipe in the following JSON format:
{{
  "recipe_name": "Name of the dish",
  "cuisine": "Type of cuisine",
  "cooking_time": "Total time in minutes",
  "difficulty": "Easy/Medium/Hard",
  "servings": "Number of servings",
  "ingredients": ["ingredient 1 with quantity", "ingredient 2 with quantity", ...],
  "instructions": ["Step 1", "Step 2", ...],
  "nutritional_info": "Brief nutritional information",
  "chef_tips": "Professional tips for best results"
}}

Make sure the recipe:
1. Uses as many of the provided ingredients as possible
2. Adheres strictly to all dietary restrictions
3. Can be completed within the time limit
4. Is practical and delicious
5. Includes clear, step-by-step instructions
"""
    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are a professional chef who creates delicious, practical recipes. Always respond with valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        max_completion_tokens=2048
    )
    return response.choices[0].message.content

if generate_button:
    if not ingredients:
        st.warning("⚠️ Please enter at least one ingredient to get recipe suggestions!")
    else:
        with st.spinner("🧑‍🍳 AI Chef is creating your perfect recipe..."):
            try:
                recipe_json = generate_recipe(ingredients, dietary_preferences, cuisine, cooking_time, servings)
                recipe = json.loads(recipe_json)
                st.success("✅ Recipe Generated Successfully!")
                st.markdown("---")
                st.markdown(f"## 🍽️ {recipe['recipe_name']}")
                info_col1, info_col2, info_col3, info_col4 = st.columns(4)
                with info_col1:
                    st.metric("🌍 Cuisine", recipe['cuisine'])
                with info_col2:
                    st.metric("⏱️ Cooking Time", f"{recipe['cooking_time']} min")
                with info_col3:
                    st.metric("📊 Difficulty", recipe['difficulty'])
                with info_col4:
                    st.metric("👥 Servings", recipe['servings'])
                st.markdown("---")
                recipe_col1, recipe_col2 = st.columns([1, 1])
                with recipe_col1:
                    st.subheader("📋 Ingredients")
                    for ingredient in recipe['ingredients']:
                        st.markdown(f"• {ingredient}")
                st.markdown("---")
                st.subheader("📊 Nutritional Information")
                st.info(recipe['nutritional_info'])
                with recipe_col2:
                    st.subheader("👨‍🍳 Instructions")
                    for idx, instruction in enumerate(recipe['instructions'], 1):
                        st.markdown(f"**Step {idx}:** {instruction}")
                st.markdown("---")
                st.subheader("💡 Chef's Tips")
                st.success(recipe['chef_tips'])
                st.markdown("---")
                st.info("💚 Enjoy your cooking! Don't forget to share your creation with friends and family!")
            except Exception as e:
                st.error(f"❌ Error generating recipe: {str(e)}")
                st.info("Please check your OpenAI API key and try again.")

st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
    <p>🤖 Powered by AI | Made with ❤️ for food lovers</p>
    <p>Perfect for college projects and GitHub portfolios!</p>
    </div>
    """,
    unsafe_allow_html=True
)