import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Jarbas 🤖")

if "openai_model" not in st.session_state:
  st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
  st.session_state.messages = [] 

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if prompt := st.chat_input("Pergunte algo ao Jarbas!"):
  instructions = """Você é um chat que reponde perguntas sobre games, 
                    e indica alguns dos melhores jogos, 
                    para se divertir, você também conhece sobre hardware, 
                    e pode indicar os melhores, com diferentes propostas de preço, 
                    que o usuário irá te passar."""
  
  st.session_state.messages.append({"role":"user", "content": prompt})  
  
  with st.chat_message("user"):
    st.markdown(prompt)
    
  with st.chat_message("assistant"):
    stream = client.chat.completions.create(
      model=st.session_state['openai_model'],
      messages=[
        {"role": "system", "content": instructions},
        {"role": "user", "content":prompt}
      ],
      stream=True,
    )
    
    response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})