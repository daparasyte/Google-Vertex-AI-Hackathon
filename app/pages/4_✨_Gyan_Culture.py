import streamlit as st
from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from vertexai.preview.language_models import TextGenerationModel
import vertexai
import json

# Load the service account json file
# Update the values in the json file with your own
with open(
    "service_account.json"
) as f:  # replace 'serviceAccount.json' with the path to your file if necessary
    service_account_info = json.load(f)

my_credentials = service_account.Credentials.from_service_account_info(
    service_account_info
)

# Initialize Google AI Platform with project details and credentials
aiplatform.init(
    credentials=my_credentials,
)

with open("service_account.json", encoding="utf-8") as f:
    project_json = json.load(f)
    project_id = project_json["project_id"]


# Initialize Vertex AI with project and location
vertexai.init(project=project_id, location="us-central1")

def main():
    st.title(':orange[Gyan Cultural Guide]')

    default_fluency = st.session_state.get("user.fluency", 3)
    fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1,
                                value=default_fluency)
    
    st.session_state["user.fluency"] = fluency

    services = [
        "Culture Info",
        "Cultural Misconduct",
    ]

    service_choice = st.selectbox("Choose a Service", options=services)
    st.divider()

    # <-------- Culture Info -------->
    if service_choice == "Culture Info":
        cols = st.columns(2)
        with cols[0]:
            country = st.text_input("Country")
        with cols[1]:
            region = st.text_input("Region or City (Optional)")

        if st.button("Create Guide"):
            with st.spinner():
                parameters = {
                    "temperature": 0.5,
                    "max_output_tokens": 1024,
                    "top_p": 0.8,
                    "top_k": 40
                }
                model = TextGenerationModel.from_pretrained("text-bison@001")
                response = model.predict(
                    f"""Please provide a brief cultural guide for someone who is in the age group 8-12 years, who should be aware when 
                visiting {country}, Specific Region (Optional): {region}. The langauge should be understandable by a person who is 
                {fluency}/10 fluent in English. This guide should include notable places to visit, popular local cuisine, something fun
                to do, common practices, and some general things. Also keep it very safe for work.

                Respond with content formatted in markdown syntax that can be displayed directly to the language learner. 
                Use \"simple language\" Do not include any other text or response besides the content of the guide.
                """,
                    **parameters
                )
            st.session_state["culture.info"] = response.text

            if "culture.info" in st.session_state:
                service_info = st.session_state["culture.info"]
                st.markdown(service_info)
    

    # <-------- Culture Misconduct -------->    
    elif service_choice == "Cultural Misconduct":
        cols = st.columns(2)
        with cols[0]:
            country = st.text_input("Country")
        with cols[1]:
            region = st.text_input("Region or City (Optional)")

        if st.button("Get Cultural Etiquette"):
            with st.spinner():
                parameters = {
                    "temperature": 0.5,
                    "max_output_tokens": 1024,
                    "top_p": 0.8,
                    "top_k": 40
                }
                model = TextGenerationModel.from_pretrained("text-bison@001")
                response = model.predict(
                    f"""Please provide a list of cultural misconduct or etiquette to be followed that a traveler should be aware of 
                when visiting {country}. Specific Region (Optional): {region}. The langauge should be understandable by a person who is 
                {fluency}/10 fluent in English.

                Respond with content formatted in markdown syntax that can be displayed directly to me. Use \"simple language\" as you 
                will be providing the information to kids (age 8-12 years). Do not include any other text or response besides the content 
                of the itinerary.
                """,
                    **parameters
                )
            st.session_state["culture.etiquette"] = response.text

            if "culture.etiquette" in st.session_state:
                service_info = st.session_state["culture.etiquette"]
                st.markdown(service_info)
    
if __name__ == "__main__":
    main()
