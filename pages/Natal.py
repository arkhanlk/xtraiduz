import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import random 

part = {
    'Estela':'',
    'J. Pedro':'',
    'Luiz':'',
    'Karina':'',
    'J. Paulo':'',
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

dice = part.keys()
random.shuffle(dice)

diced = {}
def rander():
    for k, d in zip(part.keys(), dice):
        if k != d:
            diced[k] = ''.join(chr(int(d[i*8:i*8+8],2)) for i in range(len(d)//8))
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
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))
    
# Call the word_count function with an input sentence and print the results.
if ss['btn']:
    st.write(word_count(ss['txt']))
