import pathlib
import sys

import streamlit as st

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

st.title("Welcome to ***:green[GyanAI]***")

st.markdown("""
Welcome to ***:green[GyanAI]***, your learning companion! ***:green[GyanAI]*** helps kids develop communication skills for their growth.

Imagine a world where every child can learn by interacting. ***:green[GyanAI]*** makes it happen with:
- fun personalized language learning. 
- imaginative storytelling
- cultural adventures

Join us on this exciting journey as we explore languages together. Let ***:green[GyanAI]*** be your guiding star to knowledge and growth!
""")


st.header("Activities")

expander = st.expander("Gyan Speak 📝")
expander.markdown("""
With :red[Gyan Speak], kids can read sentences word by word with the help of our AI. It's a 
special module that helps you translate text from your language to another language 
you want to learn. Not only does it translate the words, but it also gives you a detailed 
explanation to support your learning. Get ready to improve your language skills with 
:red[Gyan Speak]!

[Visit Gyan Speak](/Gyan_Speak)
""")

expander = st.expander("Gyan Chat 🤖")
expander.markdown("""
With :red[Gyan Chat] you can now interact with out Gyan assistant to learn and explore new
things together.

[Visit Gyan Chat](/Gyan_Chat)
""")

expander = st.expander("Gyan Community 💎")
expander.markdown("""
Multiple studies have shown that the roots in the ability to communicate lies in the availability of
social environments during the infancy stage. With :red[Gyan Community] you can now connect and interact 
with your peers to learn and explore new things together.

[Visit Gyan Community](/Gyan_Community)
""")

expander = st.expander("Gyan Culture ✨")
expander.markdown("""
Discover new cultures with the :red[Gyan Culture]! It's like having a guidebook that 
tells you all about different places. You can learn about their customs, and 
even find out what things you should avoid doing in different parts of the world. This 
module has everything you need to become a cultural expert!

[Visit Gyan Culture](/Gyan_Culture)
""")
