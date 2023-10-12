import streamlit as st 
from PyPDF2 import PdfWriter 
import base64
import pandas as pd

fileName = "merged-pdf.pdf"

def main():
    exception = False
    st.title("📝 Merge PDF's") 

    uploaded_file = st.file_uploader("Upload pdf files", type=("pdf"), accept_multiple_files=True) 

    if(uploaded_file):
        st.header('Files preview')
        for file in uploaded_file:
            base64_pdf = base64.b64encode(file.read()).decode('utf-8')
            pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
            with st.expander(file.name):
                st.markdown(pdf_display, unsafe_allow_html=True)
     
    if(len(uploaded_file) > 1):
        mergeSpecifiedPages = st.toggle('Merge specified pages')

        if(mergeSpecifiedPages):
            st.header('Page picker')

            df = pd.DataFrame(columns=['File', 'Page'])

            for pdf in uploaded_file:
                new_row = {"File": f'{pdf.name}', 'Page': 1}
                new_df = pd.DataFrame(new_row, index=[0])
                df = pd.concat([df, new_df], ignore_index=True)

            df = pd.DataFrame(df)
            edited_df  = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        if st.button('Merge'):
            merger = PdfWriter()

            if(len(uploaded_file) > 1):
                if(mergeSpecifiedPages):
                    df = df.reset_index()
                    for index, row in edited_df.iterrows():
                        try:
                            document = [x for x in uploaded_file if x.name == row['File']][0]
                            merger.append(fileobj=document, pages=(row['Page']-1, row['Page']))
                        except IndexError:
                            st.error('Please make sure that the file names/page numbers are valid')
                            exception = True
                            break
                else:
                    for pdf in uploaded_file:
                        merger.append(pdf)

                merger.write(fileName)
                merger.close()

                if(not exception):
                    with open(fileName, 'rb') as f:
                        file_data = f.read()
                        st.download_button(
                            label="Download PDF",
                            file_name=fileName,
                            mime="application/pdf",
                            data=file_data,)

if __name__ == '__main__':
    main()
