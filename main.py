import streamlit as st 
import PyPDF2
from PyPDF2 import PdfWriter 

st.title("📝 Merge PDF's") 
uploaded_file = []
uploaded_file = st.file_uploader("Upload pdf files", type=("pdf"), accept_multiple_files=True) 
fileName = "merged-pdf.pdf"
if(len(uploaded_file) > 0):
    merger = PdfWriter()
    for pdf in uploaded_file:
        merger.append(pdf)

    merger.write(fileName)
    merger.close()

    with open(fileName, 'rb') as f:
        file_data = f.read()
        st.download_button(
            label="Download PDF",
            file_name=fileName,
            mime="application/pdf",
            data=file_data,) 
