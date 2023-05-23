import streamlit as st
import docx2txt
import pandas as pd
import PyPDF2
import aspose.words as aw
from my_transformer_function import MyTransformer,clean_it
import pickle   
from pyresparser import ResumeParser


pipeline = pickle.load(open('pipeline.pkl','rb'))

doc_type_warning = False
unsupported_warning = False

report_df=pd.DataFrame(columns=['File','Texts','Resume Type'])

with st.form("my-form", clear_on_submit=True):
    files = st.file_uploader("upload file",accept_multiple_files=True)
    submitted = st.form_submit_button("submit")

for file in files:
    texts=''
    
    doc_type = file.name.split('.')[-1]

    if doc_type == 'docx':
        texts = docx2txt.process(file)
        
    elif doc_type == 'pdf':    
                   
        pdf = PyPDF2.PdfReader(file)
        for i in range(len(pdf.pages)):
            texts += pdf.pages[i].extract_text()
            
    elif doc_type == 'doc':
        
        doc_type_warning = True
        prom_txt = 'This document was truncated here because it was created in the Evaluation Mode.Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/'

        texts = aw.Document(file).get_text()
        texts = texts.replace(prom_txt,"")
    
    else:
        unsupported_warning = True
        
    report_df.loc[len(report_df),['File','Texts']] = file.name,texts

        
if doc_type_warning:
    st.write("'.doc' type may not work as expected, try using '.docx' or '.pdf'")
    
if unsupported_warning:
    st.write("Document type is not supported, '.docx' or '.pdf' will work")
        


 
if len(report_df) > 0   :
    report_df['Resume Type'] = pipeline.predict(report_df['Texts'])
    st.dataframe(report_df.iloc[:,[0,2]])
    
    
    

    

