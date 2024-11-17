import streamlit as st
import requests
api = "https://storiatatts.agreeableground-aec2017e.australiaeast.azurecontainerapps.io/generate-audio"

st.write(""" 
# Phonemically Accurate Cebuano Text-to-Speech
""")

text = st.text_input(
    "Write the text to generate to speech",
    placeholder = "Input text here"
    )

st.button("Generate", type="primary")
if st.button:
    words = text.split()
    tokens = []
    i = 0
    for word in words:
        chars = list(word)
        if chars[-1] == '.':
            chars.remove('.')
            tokens.append(''.join(chars))
            tokens.append('.')
        else:
            tokens.append(word)
        i += 1
    st.write(tokens)


    # response = requests.post(api, json=data)

    # if response.status_code == 200:
    #     audio = response.content.decode('utf-8').strip('b"\'')
    #     st.write(audio) 
    #     st.audio(audio, format="audio/mp3")  






