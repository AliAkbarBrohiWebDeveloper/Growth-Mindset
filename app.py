import streamlit as st

import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

# custom css
st.markdown(
    """
        <style>
        .stApp{
               background-color:dark;
              color:black
         }
         </style>
          """,
          unsafe_allow_html=True
             
)

# title and description
st.title(" DataSweeper sterling integreter by Ali Akbar Brohi ")
st.write("Transform your files between CVS and Excel formates with built in data cleaning")

uploadded_files=st.file_uploader("Upload Your files accept CVS and Excel:",type=["cvs","xlsx"],accept_multiple_files=(True))

if uploadded_files:
    for file in uploadded_files:
        file_ext=os.path.splitext(file.name)[-1].lower()
        if file_ext==".csv":
            df=pd.read_csv(file)
        elif file_ext=="xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"UnSupported file type: {file_ext}")
            continue


        #file details
        st.write("preview the head of the data frame ")
        st.dataframe(df.head())

        st.subheader("Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1,col2=st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from the file:{file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("duplicates removed")

                    with col2:
                        if st.button(f"Fill missing values for {file.name}") :
                            numeric_cols=df.select_dtypes(include=["number"]).columns
                            df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean)
                            st.write("Missing valuse have been filled")
                            st.subheader("select columns to keep")
                            columns=st.multiselect(f"Choose columns for {file.name}",df.columns,default=df.columns)
                            df=df[columns]
                            


                            #data visualization

                            st.subheader("Data visualaization")
                            if st.checkbox(f"Show visualaization for {file.name}"):
                                st.bar_chart(df.select_dtypes (include='number').iloc[:,:2])


                                st.subheader("conversion options")
                                conversion_type=st.radio(f"Convert {file.name} to: ",['CSV','Excel'],key=file.name )
                                if st.button(f"Convert {file.name}"):
                                   buffer=BytesIO() 
                                   if conversion_type=="CSV":
                                       df.to.to_csv(buffer,index=False)
                                       file_name=file.name.replace(file_ext,".csv")
                                       mime_type="text/csv"
                                   elif conversion_type=="Excel":
                                       df.to_excel(buffer,index=False)
                                       file_name=file.name.replace(file_ext,".xlsx")
                                       mime_type="application/vnd.openxmlformates-officedocument.spreadsheetml.sheet"
                                       buffer.seek(0)

                                       st.download_button(
                                           label=f"Download {file.name} as {conversion_type}",
                                           data=buffer,
                                           file_name=file_name,
                                           mime=mime_type
                                       )
                                   st.success("All files proccced successfully")

