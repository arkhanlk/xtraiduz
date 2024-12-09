import streamlit as st
from streamlit import session_state as ss
import pandas as pd

ss['txt'] = st.text_area('Cola o código aqui')
ss['btn'] = st.button('Clique para decifrar')
def word_count(str):
    res = ''.join(format(ord(i), '08b') for i in ss['txt'])
    
# Call the word_count function with an input sentence and print the results.
if ss['btn']:
    st.write(res)
