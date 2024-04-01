import os

import streamlit as st

from app import input_open_api_key
from app import invoke
from app import show_chat
from app import show_result

from src.template import TEMPLATE_DICT
from src.password import PASSWORD_DICT


def input_template():
    template = st.text_area("プロンプトテンプレート", list(TEMPLATE_DICT.values())[-1], height=512)
    st.session_state['template'] = template


def input_password():
    password = st.text_input("パスワード", list(PASSWORD_DICT.values())[-1])
    st.session_state['password'] = password


def main():
    st.title('NevilleQuest: Password Pursuit')
    st.write('Nevilleからパスワードを聞き出してください')

    input_open_api_key()

    if 'open_api_key' in st.session_state:
        os.environ["OPENAI_API_KEY"] = st.session_state.open_api_key

        input_template()
        input_password()

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