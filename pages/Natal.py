import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import random 

ss['txt'] = st.text_area('Cola o código aqui')
ss['btn'] = st.button('Clique para decifrar')

vv = str()
def word_count(s):
    global vv
    var = list((ss['txt']).split(','))
    for v in var:
        st.write(chr(int(v)))
        vv = str(vv) + str(chr(int(v)))
    st.write(vv)
    
# Call the word_count function with an input sentence and print the results.
if ss['btn']:
    st.write(word_count(ss['txt']))
