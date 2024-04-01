import os

import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

from src.template import TEMPLATE_DICT
from src.password import PASSWORD_DICT


def input_open_api_key():
    if 'open_api_key' not in st.session_state:
        open_api_key = st.text_input("OpenAI APIキー", type='password')
        if open_api_key:
            st.session_state.open_api_key = open_api_key
            st.rerun()


def change_level():
    level = st.selectbox(
        "レベルを選択",
        ("leve10", "leve11")
    )

    if 'current_level' in st.session_state and st.session_state.current_level != level:
        del st.session_state['current_user_input']
        del st.session_state['response']

    st.session_state['template'] = TEMPLATE_DICT[level]
    st.session_state['password'] = PASSWORD_DICT[level]

    st.session_state.current_level = level


def show_chat():
    if 'current_user_input' in st.session_state:
        with st.chat_message("Player"):
            st.write(st.session_state.current_user_input)
    if 'response' in st.session_state:
        with st.chat_message("Neville"):
            st.write(st.session_state.response)


def show_result(answer_check, answer):
    if answer_check and answer:
        if answer == st.session_state['password']:
            st.balloons()
            st.success('正解!', icon="⭕️")
        else:
            st.error('不正解', icon="❌")


def invoke(user_input):
    st.session_state.current_user_input = user_input

    prompt_template = PromptTemplate(
        template=st.session_state['template'],
        input_variables=["password", "user_input"]
    )

    prompt = prompt_template.format(
        password=st.session_state['password'],
        user_input=user_input
    )

    llm = OpenAI(temperature=0.9)
    response = llm.predict(prompt)
    return response



def main():
    st.title('NevilleQuest: Password Pursuit')
    st.write('Nevilleからパスワードを聞き出してください')

    input_open_api_key()

    if 'open_api_key' in st.session_state:
        os.environ["OPENAI_API_KEY"] = st.session_state.open_api_key

        change_level()

        user_input = st.text_input("プロンプト")
        submit = st.button('送信')

        if submit:
            response = invoke(user_input)
            st.session_state.response = response

        show_chat()

        answer = st.text_input("パスワード")
        answer_check = st.button('答え合わせ')

        show_result(answer_check, answer)


if __name__ == '__main__':
    main()