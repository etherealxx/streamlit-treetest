#autoabsen

import streamlit as st
# import subprocess

# tree = subprocess.getoutput('tree /')

import os

# st.write("pat")

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        st.write('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            st.write('{}{}'.format(subindent, f))


start_directory = "/mount/src"
list_files(start_directory)

# st.write(tree)