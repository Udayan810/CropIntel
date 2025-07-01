import streamlit as st
from agents.farmer_advisor import load_model, predict_yield
from agents.market_researcher import analyze_market_trends
from utils.db_utils import init_db, insert_prediction
from dashboard.dashboard import render_dashboard
from utils.recommendition import recommend_crop, recommend_fertilizer

# Initialize DB
init_db()

st.set_page_config(page_title="🌱 AI Sustainable Farming", layout="centered")
st.title("🌾 AI-Powered Sustainable Farming System")

menu = st.sidebar.selectbox("Choose a Role", ["Farmer Advisor", "Market Researcher", "📊 Prediction Dashboard","🌾 Crop Recommendation", "🧪 Fertilizer Recommendation", "🧑‍🌾 Farming Assistant"])
#menu = st.sidebar.selectbox("Menu", ["🏠 Home", "🌱 Make Prediction", "📊 Prediction Dashboard", ])

if menu == "Farmer Advisor":
    st.header("📊 Predict Crop Yield")
    soil_ph = st.slider("Soil pH", 4.0, 9.0, 6.5)
    moisture = st.slider("Soil Moisture (%)", 0.0, 100.0, 25.0)
    temperature = st.slider("Temperature (°C)", 5.0, 45.0, 27.0)
    rainfall = st.number_input("Rainfall (mm)", value=50.0)
    fertilizer = st.number_input("Fertilizer Usage (kg)", value=80.0)
    pesticide = st.number_input("Pesticide Usage (kg)", value=5.0)
    crop_type = st.selectbox("Crop Type", ["Wheat", "Rice", "Corn", "Soybean"])

    if st.button("🚜 Predict Yield"):
        crop_map = {'Wheat': 0, 'Rice': 1, 'Corn': 2, 'Soybean': 3}
        encoded_crop = crop_map[crop_type]

        features = [
            soil_ph, moisture, temperature, rainfall,
            fertilizer, pesticide, encoded_crop
        ]

        try:
            model = load_model()
            yield_pred = predict_yield(model, features)

            st.success(f"Predicted Yield: 🌾 **{yield_pred:.2f} tons/hectare**")

            # Only pass 8 values as expected by the DB
            insert_prediction([
                soil_ph,
                moisture,
                temperature,
                rainfall,
                fertilizer,
                pesticide,
                crop_type,
                yield_pred
            ])
        except Exception as e:
            st.error(f"Prediction failed: {e}")


elif menu == "Market Researcher":
    st.header("📈 Market Trend Analysis")
    market_data = analyze_market_trends()
    if isinstance(market_data, str):
        st.error(market_data)
    else:
        st.dataframe(market_data)

elif menu == "📊 Prediction Dashboard":
    render_dashboard()

elif menu == "🌾 Crop Recommendation":
    st.subheader("🌾 Intelligent Crop Recommendation")
    soil_ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, step=0.1)
    moisture = st.slider("Soil Moisture (%)", 0, 100)
    temperature = st.slider("Temperature (°C)", 0, 50)
    rainfall = st.slider("Rainfall (mm)", 0, 500)

    if st.button("Recommend Crop"):
        crop = recommend_crop(soil_ph, moisture, temperature, rainfall)
        st.success(f"🌱 Recommended Crop: **{crop}**")
elif menu == "🧪 Fertilizer Recommendation":
    st.subheader("🧪 Smart Fertilizer Recommendation")
    crop_type = st.selectbox("Select Crop", ["Rice", "Wheat", "Maize", "Groundnut", "Others"])

    if st.button("Recommend Fertilizer"):
        fertilizer = recommend_fertilizer(crop_type)
        st.success(f"🧪 Recommended Fertilizer for {crop_type}: **{fertilizer}**")

elif menu == "🧑‍🌾 Farming Assistant":
    
    import os
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory
    from langchain_groq import ChatGroq
    from dotenv import load_dotenv

    st.subheader("🧑‍🌾 Ask the Farming Assistant")
    load_dotenv()

    llm = ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Get user input
    user_input = st.chat_input("Ask something about farming...")

    if user_input:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response
        prompt = f"""You are a knowledgeable agricultural assistant helping farmers with real, practical advice.
Only talk about farming topics like crops, fertilizers, irrigation, pest control, and yield.
Don't talk about human emotions or random facts. Focus only on agriculture.

User: {user_input}
Assistant:"""

        reply = st.session_state.conversation.run(prompt)

        # Show assistant response
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
elif menu == "🧑‍🌾 Farming Assistant":

    import os
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory
    from langchain_groq import ChatGroq
    from deep_translator import GoogleTranslator
    from dotenv import load_dotenv
    from googletrans import Translator

    st.subheader("🧑‍🌾 Ask the Farming Assistant")
    load_dotenv()

    llm = ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    translator = Translator()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationBufferMemory(),
            verbose=False
        )

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Get user input
    user_input = st.chat_input("Ask something about farming (in any language)...")

    if user_input:
        # # Detect and translate to English
        # detected_lang = translator.detect(user_input).lang
        # user_input_en = translator.translate(user_input, dest='en').text
        

        # Detect language and translate to English
        detected_lang = GoogleTranslator(source='auto', target='en').detect(user_input)
        user_input_en = GoogleTranslator(source='auto', target='en').translate(user_input)

        # Assistant generates response
        reply_en = st.session_state.conversation.run(prompt)

        # Translate back to original language
        reply_translated = GoogleTranslator(source='en', target=detected_lang).translate(reply_en)


        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant response
        prompt = f"""You are a knowledgeable agricultural assistant helping farmers with real, practical advice.
Only talk about farming topics like crops, fertilizers, irrigation, pest control, and yield.
Don't talk about human emotions or random facts. Focus only on agriculture.

User: {user_input_en}
Assistant:"""

        reply_en = st.session_state.conversation.run(prompt)

        # Translate reply back to original language
        reply_translated = translator.translate(reply_en, dest=detected_lang).text

        # Show assistant response
        st.session_state.messages.append({"role": "assistant", "content": reply_translated})
        with st.chat_message("assistant"):
            st.markdown(reply_translated)



