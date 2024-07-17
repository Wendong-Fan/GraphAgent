import streamlit as st
import os

st.title("File Path Input")


# this script can get file context when running locally by file path

# Text input for file path
file_path = st.text_input("Enter the file path")

if file_path:
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_content = file.read()
            st.write("File content:")
            st.write(file_content.decode("utf-8"))
    else:
        st.error("File does not exist")



####################################################################
# multiple paths

# import streamlit as st
# import os

# st.title("Multiple File Path Input")

# # Multi-line text input for file paths
# file_paths_input = st.text_area("Enter the file paths, one per line")

# if file_paths_input:
#     file_paths = file_paths_input.split("\n")  # Split the input into individual paths
#     for file_path in file_paths:
#         file_path = file_path.strip()  # Remove any extra whitespace
#         if file_path:  # Check if the path is not empty
#             st.write(f"Processing file: {file_path}")
#             if os.path.exists(file_path):
#                 with open(file_path, "rb") as file:
#                     file_content = file.read()
#                     st.write("File content:")
#                     st.write(file_content.decode("utf-8"))
#             else:
#                 st.error(f"File does not exist: {file_path}")




