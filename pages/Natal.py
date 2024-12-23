import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import random 

_ = """
part = {
    'Estela':'',
    'JPedro':'',
    'Luiz':'',
    'Karina':'',
    'JPaulo':'',
    'Duda':'',
    'Eliana':'',
    'Vitor':'',
    'Mila':'',
    'Iolanda':'',
    'Alessandra':'',
    'Paulinho':'',
    }

dice = list(part.keys())
random.shuffle(dice)

diced = {}
def rander():
    for k, d in zip(list(part.keys()), dice):
        if k != d:
            diced[k] = [ord(c) for c in list(d)]
            st.success(k)
        else:
            st.warning(k)
    st.write(diced)

z = st.button('rand')
if z:
    rander()
""";

ss['txt'] = st.text_area('Cola o código aqui')
ss['btn'] = st.button('Clique para decifrar')

vv = str()
def word_count(s):
    global vv
    var = list(str(ss['txt']).strip().split(','))
    for v in var:
        st.write(chr(int(v)))
        vv = str(vv) + str(chr(int(v)))
    st.write(vv)
    
# Call the word_count function with an input sentence and print the results.
if ss['btn']:
    st.write(word_count(ss['txt']))
