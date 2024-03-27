import os

import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

from src.template import TEMPLATE_DICT
from src.password import PASSWORD_DICT


def main():
    st.title('NevilleQuest: Password Pursuit')
    st.write('Nevilleからパスワードを聞き出してください')

    if 'open_api_key' not in st.session_state:
        open_api_key = st.text_input("OpenAI APIキー", type='password')
        if open_api_key:
            st.session_state.open_api_key = open_api_key
            st.rerun()

    if 'open_api_key' in st.session_state:
        os.environ["OPENAI_API_KEY"] = st.session_state.open_api_key

        level = st.selectbox(
            "レベルを選択",
            ("leve10", "leve11")
        )

        if 'current_level' in st.session_state and st.session_state.current_level != level:
            del st.session_state['current_user_input']
            del st.session_state['response']

        template = TEMPLATE_DICT[level]
        password = PASSWORD_DICT[level]

        st.session_state.current_level = level

        user_input = st.text_input("プロンプト")
        submit = st.button('送信')

        if submit and \
                ('current_user_input' not in st.session_state or user_input != st.session_state.current_user_input):
            st.session_state.current_user_input = user_input

            prompt_template = PromptTemplate(
                template=template,
                input_variables=["password", "user_input"]
            )

            prompt = prompt_template.format(
                password=password,
                user_input=user_input
            )

            llm = OpenAI(temperature=0.9)
            response = llm.predict(prompt)
            st.session_state.response = response

        if 'current_user_input' in st.session_state:
            with st.chat_message("Player"):
                st.write(st.session_state.current_user_input)
        if 'response' in st.session_state:
            with st.chat_message("Neville"):
                st.write(st.session_state.response)

        answer = st.text_input("パスワード")
        answer_check = st.button('答え合わせ')

        if answer_check and answer:
            if answer == password:
                st.balloons()
                st.success('正解!', icon="⭕️")
            else:
                st.error('不正解', icon="❌")


if __name__ == '__main__':
    main()