import streamlit as st
import requests
api = "https://storiatatts.agreeableground-aec2017e.australiaeast.azurecontainerapps.io/generate-audio"
from conversions import convert, split_into_syllables

st.write(""" 
# Phonemically Accurate Cebuano Text-to-Speech
""")

text = st.text_input(
    "Write the text to generate phonemic syllable tokens",
    placeholder = "Input text here"
    )

st.button("Generate", type="primary")
col1, col2 = st.columns(2)
if st.button:
    with col1:
        st.write("## Words")
        st.write(convert(text))
    with col2:
        st.write("## Syllables")
        st.write(split_into_syllables(convert(text)))


    # words = text.split()
    # tokens = []
    # i = 0
    # for word in words:
    #     chars = list(word)
    #     if chars[-1] == '.':
    #         chars.remove('.')
    #         tokens.append(''.join(chars))
    #         tokens.append('.')
    #     else:
    #         tokens.append(word)
    #     i += 1
    # st.write(tokens)


    # response = requests.post(api, json=data)

    # if response.status_code == 200:
    #     audio = response.content.decode('utf-8').strip('b"\'')
    #     st.write(audio) 
    #     st.audio(audio, format="audio/mp3")  






