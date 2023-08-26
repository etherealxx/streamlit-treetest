import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import os
import platform

if 'default_starting_directory' not in st.session_state:
    if platform.system() == "Windows": # localhost
        st.session_state.default_starting_directory = "E:\\"
    elif platform.system() == "Linux": # deployed
        st.session_state.default_starting_directory = "/"

if 'starting_directory' not in st.session_state:
    st.session_state.starting_directory = st.session_state.default_starting_directory

if 'group_size' not in st.session_state:
    st.session_state.group_size = 5

starting_directory = st.session_state.starting_directory

def buttonclick(foldername):
    global starting_directory
    print(f'Clicked button with path: {foldername}')
    st.session_state.starting_directory = os.path.join(st.session_state.starting_directory, foldername)
    starting_directory = st.session_state.starting_directory
    print(f"now starting directory is: {starting_directory}")

osdir_result = []
folder_list = []
file_list = []
global_iterable = 0

container_with_border_style = """
        {
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px)
        }
        """

def walkdown():
    print("debug walkdown")
    global starting_directory
    global folder_list
    global file_list
    folder_list, file_list = [], []
    while True:
        try:
            for fileorfol in os.listdir(starting_directory):
                # osdir_result.append(fileorfol)
                if os.path.isdir(os.path.join(starting_directory, fileorfol)):
                    folder_list.append(fileorfol)
                elif os.path.isfile(os.path.join(starting_directory, fileorfol)):
                    file_list.append(fileorfol)
            break
        except (PermissionError, FileNotFoundError) as e:
            print(str(e))
            st.cache_data.clear()
            st.session_state.starting_directory = st.session_state.default_starting_directory
            starting_directory = st.session_state.starting_directory

# walkdown()

group_size = st.slider("Folders per row", value=st.session_state.group_size, min_value=1, max_value=10)
st.session_state.group_size = group_size

with stylable_container(key="container_with_border",css_styles=container_with_border_style):
    walkdown()
    headercol, buttoncol = st.columns([8,3])
    folder_sub = headercol.subheader(f"Folders in {starting_directory}")
    backbutton = buttoncol.button("⬆️")
    if backbutton:
        st.session_state.starting_directory = os.path.dirname(st.session_state.starting_directory)
        starting_directory = st.session_state.starting_directory
        print(f"going back to: {starting_directory}")
        folder_sub.subheader(f"Folders in {starting_directory}")
        walkdown()

    # Loop through the list and print in groups of 5
    # for i in range(0, len(folder_list), group_size):
    #     group = folder_list[i:i+group_size]
    #     if len(group) == 1:
    #         st.button(group[0])
    #     else:
    #         with st.container():
    #             if len(group) == 2:
    #                 col1, col2 = st.columns(2)
    #             elif len(group) == 3:
    #                 col1, col2, col3 = st.columns(3)
    #             elif len(group) == 4:
    #                 col1, col2, col3, col4 = st.columns(4)
    #             elif len(group) == 5:
    #                 col1, col2, col3, col4, col5 = st.columns(5)

    #         for i, folder in enumerate(group):
    #             exec(f"col{i+1} = st.button(\"{folder}\")")

    for i in range(0, len(folder_list), group_size):
        group = folder_list[i:i+group_size]
        
        with st.container():
            num_cols = len(group)
            cols = st.columns(num_cols)
            
            for j, folder in enumerate(group):
                cols[j].button(folder, key=f"button{global_iterable}", on_click=buttonclick, args=(folder,))
                global_iterable += 1

with stylable_container(key="container_with_border",css_styles=container_with_border_style):
    walkdown()
    st.subheader(f"Files in {starting_directory}")
    
    for i in range(0, len(file_list), group_size):
        group = file_list[i:i+group_size]
        
        with st.container():
            num_cols = len(group)
            cols = st.columns(num_cols)
            
            for j, folder in enumerate(group):
                cols[j].button(folder)
