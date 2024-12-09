import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import random 

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
    'Laura':'',
    'Julia':'',
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

ss['txt'] = st.text_area('Cola o código aqui')
ss['btn'] = st.button('Clique para decifrar')

def word_count(s):
    var = (ss['txt']).split(',')
    for c in (ss['txt']).split(','):
        return chr(c)
    
# Call the word_count function with an input sentence and print the results.
if ss['btn']:
    st.write(word_count(ss['txt']))
