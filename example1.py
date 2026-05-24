import streamlit as st

st.title("Hello, Streamlit! This is a Nested Buttons Example")

if 'button1_clicked' not in st.session_state:
    st.session_state.button1_clicked = False

if st.button("Button 1"):
    st.write("You clicked Button 1!")
    st.session_state.button1_clicked = True

if st.session_state.button1_clicked:
    if 'button1_1_clicked' not in st.session_state:
        st.session_state.button1_1_clicked = False

    if st.button("Button 1.1"):
        st.write("You clicked Button 1.1!")
        st.session_state.button1_1_clicked = True

    if 'button1_2_clicked' not in st.session_state:
        st.session_state.button1_2_clicked = False

    if st.button("Button 1.2"):
        st.write("You clicked Button 1.2!")
        st.session_state.button1_2_clicked = True
else:
    st.write("You haven't clicked Button 1 yet.")
    
    

