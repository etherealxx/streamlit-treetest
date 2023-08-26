#autoabsen

import streamlit as st
import subprocess

tree = subprocess.getoutput('tree /')
st.write(tree)