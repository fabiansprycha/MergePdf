import streamlit as st 
from PyPDF2 import PdfWriter 
import base64
import pandas as pd

fileName = "merged-pdf.pdf"

def main():
    exception = False
    st.title("📝 Merge PDF's") 

    uploaded_file = st.file_uploader("Upload PDF files", type=("pdf"), accept_multiple_files=True) 
    if(uploaded_file):
        st.divider()
        st.caption('By default, whole PDF files will be merged into one file.')
        st.caption('')
        st.caption(' If you want to merge specific pages from a PDF file mark this option:')

        mergeSpecifiedPages = st.toggle('Merge specific pages')

    if(len(uploaded_file) > 1):
        if(mergeSpecifiedPages):
            st.divider()
            st.header('Page picker')
            st.caption('Specify what the merged PDF should look like by adding a new row with a file name and page. Right now new PDF will be created from the first pages of all uploaded files. For example, add a new row with the first PDF file name and page range \'2-3\' - then a new PDF will be created from the first pages of all uploaded files and pages 2 and 3 of the first file at the end.')

            df = pd.DataFrame(columns=['File', 'Page'])

            for pdf in uploaded_file:
                new_row = {"File": f'{pdf.name}', 'Page': "1"}
                new_df = pd.DataFrame(new_row, index=[0])
                df = pd.concat([df, new_df], ignore_index=True)

            df = pd.DataFrame(df)
            edited_df  = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        
        st.caption('')
        st.divider()
        if st.button('Merge'):
            merger = PdfWriter()

            if(len(uploaded_file) > 1):
                if(mergeSpecifiedPages):
                    df = df.reset_index()
                    for index, row in edited_df.iterrows():
                        try:
                            document = [x for x in uploaded_file if x.name == row['File']][0]
                            if('-' in str(row['Page'])):
                                pages = row['Page'].split('-')
                                for page in pages:
                                    merger.append(fileobj=document, pages=(int(page)-1, int(page)))
                            else:
                                merger.append(fileobj=document, pages=(int(row['Page'])-1, int(row['Page'])))
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
