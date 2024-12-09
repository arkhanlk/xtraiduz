import streamlit as st
from streamlit import session_state as ss
import pandas as pd

ss['txt'] = st.text_area('Cola o código aqui')
ss['btn'] = st.button('Clique para decifrar')
def word_count(str):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
    
# Call the word_count function with an input sentence and print the results.
if ss['btn']:
    st.write(word_count(ss['txt']))
