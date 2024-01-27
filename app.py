import re
from openai import OpenAI
import os
import streamlit as st
import datetime

st.title("Bem vinda à Glowz Beauty Lounge!")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
     st.session_state.messages = []
     lista_servicos =  " \n2 - Tirar dúvidas sobre beleza ou autoestima. \n3 - Falar com uma atendente humana."
     st.session_state.messages = [{'role':'system', 'content':'Você é a Bela, assistente virtual do salão de beleza chamado Glowz Beauty Lounge. No primeiro contato voce deve apresentar o salão de uma forma positiva, usando até 60 palavras e depois deve retornar o seguinte texto. Como posso te ajudar hoje? 1 - Agendar um procedimento. 2 - Conversar sobre dicas de beleza. 3 - Falar com uma atendente humana.'}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
print(st.session_state.messages)

if prompt := st.chat_input("Conversar..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Obtenha a hora atual
hora_atual = datetime.datetime.now()

# Formate a hora atual como uma string usando strftime
formato = "%Y-%m-%d %H:%M:%S"  # Exemplo de formato com barras, dois pontos e traços
hora_formatada = hora_atual.strftime(formato)

# Remova barras, dois pontos e traços usando expressão regular
hora_formatada_sem_caracteres_especiais = re.sub(r'[-:/]', '', hora_formatada)

# Salvando as mensagens em um arquivo de texto
with open(f"conversa_{hora_formatada_sem_caracteres_especiais}.txt", "w", encoding="utf-8") as file:
    for message in st.session_state.messages:
        file.write(f"{datetime.datetime.now()} - {message['role']}: {message['content']}\n")