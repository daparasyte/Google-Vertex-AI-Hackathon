import streamlit as st
from google.auth import credentials
from google.oauth2 import service_account
import google.cloud.aiplatform as aiplatform
from vertexai.preview.language_models import ChatModel, TextGenerationModel, InputOutputTextPair
import vertexai
import json  # add this line
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header

import PyPDF2
import speech_recognition as sr
import re
from audio_recorder_streamlit import audio_recorder
import time
from gtts import gTTS
from io import BytesIO
import base64
import pylev


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
    tab1, tab2 = st.tabs(["Gyan Speak", "Gyan Create"])

    with tab1:
        st.title(":violet[Gyan Speak]")

        default_fluency = st.session_state.get("user.fluency", 3)
        

        fluency = st.sidebar.slider("Fluency", min_value=1, max_value=10, step=1,
                                    value=default_fluency)
        
        st.session_state["user.fluency"] = fluency

        pdf = st.file_uploader("Load pdf: ", type=['pdf'])

        if pdf is not None:
            if pdf is not None:
                pdf_reader = PyPDF2.PdfReader(pdf)

                text = ""
                for page in pdf_reader.pages:
                    text+= page.extract_text()

                text = text.replace('\n', ' ')
                text = re.sub('\s+', ' ', text) 

            st.header(f"""{text}""")

        audio_bytes = audio_recorder(
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="user",
            icon_size="6x",
            text="Record Your Voice",
            pause_threshold=2.0, 
            sample_rate=41_000
        )

        if audio_bytes:
          recording = st.audio(audio_bytes, format="audio/wav")
          with st.spinner("Processing..."):
            srec = sr.Recognizer()
            asr = srec.recognize_google(audio)
            
            a = text.split(" ")
            b = asr.split(" ")
            diff = pylev.levenshtein(a,b)   # comparing the spoken text with actual text

            x=[]
            y=[]
            x = diff.extract(a)    # extracting correct words from actual text
            y = diff.extract(b)    # extracting incorrect words from spoken text

            answer = f"The pronounciation is {', '.join(x)} not {', '.join(y)}!"
                tts = gTTS(answer, lang='en', tld='co.in')
                tts.save('answer.wav')
                audio_byte = BytesIO()
                tts.write_to_fp(audio_byte)
                audio_byte.seek(0)

                st.audio(audio_byte, format="audio/wav")

    with tab2:
        
        st.title(":violet[Gyan Create]")

        concept = st.text_input("What kind of story would you like?")

        def generator(fluency, concept):
            parameters = {
                "temperature": 0.7,
                "max_output_tokens": 128,
                "top_p": 0.8,
                "top_k": 40
            }
            model = TextGenerationModel.from_pretrained("text-bison@001")
            storyteller = model.predict(
                f"""Create a \"very short\" and simple, engaging story suitable for a language learner at a fluency level of {fluency} / 10. Fluency of 1 / 10 should be story a child (age 5 years old) could understand. Fluency of 10 / 10 should contain sophisticated language that a 10 year old can understand. The story should revolve around the theme: \"{concept}\".           
            """,
                **parameters
            )
            generated = storyteller.text
            return generated

        if st.button("Generate Story"):
            with st.spinner("Processing..."):
                data = generator(fluency, concept)
                st.header(data)
            

if __name__ == "__main__":
    main()
        
