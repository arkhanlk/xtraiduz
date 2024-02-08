import streamlit as st
import tika
tika.initVM()
from tika import parser
from deep_translator import GoogleTranslator
from stqdm import stqdm
import string
import re
import time
import math

st.set_page_config(
    page_title='Xtraiduz - Extrai & Traduz',
    page_icon='📖',)

#### CODE AFTER THIS LINE ####
tbET, = st.tabs(['Extrair & Traduzir'])

# gerando arquivo
with tbET:
    st.write('# Faça upload de um arquivo 📖 (ePub ou PDF)')
#    st.sidebar.success('Escolha uma função acima')

    uploaded_file = st.file_uploader('Escolher arquivo', accept_multiple_files=False)
    if uploaded_file:
        
        out = 'original.txt'
        parsed = parser.from_file(uploaded_file)
        content = parsed['content']
        with open(out, 'w', encoding='utf-8') as fout:
            fout.write(content)
            fout.close()
        f = open('original.txt', 'r', encoding='utf8')
        
        if 'original' not in st.session_state:
            st.session_state['original'] = f

        lines = f.readlines()
        c = 0
        z = str()
        with st.expander('Prévia do texto'):
            for line in lines:
                if len(line) >= 3:
                    c += len(line)
                    z += (line + '\n')
                    st.markdown(line)

        st.download_button(
            label='Download texto extraído',
            data=z,
            file_name=out,
            mime='text')

        st.info(f'Quantidade de letras nesse texto, considerando os espaços: {c}', icon='ℹ️')
        st.warning('O máximo de letras permitidas por dia são 300000', icon='⚠️')

        trad = st.button('Traduzir!', key='traduzido')
        if trad:
            traduzido = []
            for line in stqdm(lines):
                time.sleep(0.01)
                if len(line) >= 3:
                    translated = GoogleTranslator(source='auto', target='pt').translate(line)
                    traduzido.append(translated)

            zz = str()
            with st.expander('Prévia da tradução'):
                for ln in traduzido:
                    zz += str(ln + '\n')
                    st.markdown(ln + '\n')
            
            st.download_button(
            label='Download texto traduzido',
            data=zz,
            file_name='traduzido.txt',
            mime='text')
