import streamlit as st
import pandas as pd
import numpy as np
import base64
st.beta_set_page_config(layout='wide')


def main():

    st.title('Delinquent Exploration')

    """
    Created by Mark Kinyanjui

    """

    """
    # Step 1: Import Data
    """
    df = st.file_uploader(
        'Import dataset - data has already been cleaned and matched')

    if df is not None:
        df = pd.read_excel(df)
        df['Units'] = 1
        df['Company'] = 'AmCap'
        if st.button('Display Uploaded Data'):
            st.write(df)

        """
        # Step 2: 10,000ft View
        """
        row1_space1, row1_1, row1_space2, row1_2, row1_space3, row1_3 = st.beta_columns(
            (.001, 1, .001, 1, .001, 1))

        with row1_1:
            all_divisions = df[[
                'Division Name', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
            all_divisions = all_divisions.groupby(
                ['Division Name', 'Delinquent Reason Descriptions']).sum('Units').reset_index()
            all_divisions = all_divisions[all_divisions['Delinquent Reason Descriptions']
                                          != 'National Emergency Declaration     ']
            st.write(all_divisions)

        with row1_2:
            all_divisions = df[[
                'Division Name', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
            all_divisions = all_divisions.groupby(
                ['Division Name', 'Delinquent Reason Descriptions']).sum('Units').reset_index()
            all_divisions = all_divisions[all_divisions['Delinquent Reason Descriptions']
                                          == 'National Emergency Declaration     ']
            st.write(all_divisions)
        with row1_3:
            del_data = df.groupby(['Branch Name']).sum(
                'Units').reset_index()
            del_data = del_data[[
                'Branch Name', 'Mortgage Amount', 'Units']]
            st.write(del_data)

        if st.button('Display Loan Officer Data'):
            row01_space1, row01_1, row01_space2, row01_2, row01_space3, row01_3 = st.beta_columns(
                (.001, 1, .001, 1, .001, 1))
            with row01_1:
                branch_data = df[[
                    'Loan Officer', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                branch_data = branch_data.groupby(['Loan Officer', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()

                branch_data = branch_data[branch_data['Delinquent Reason Descriptions']
                                          != 'National Emergency Declaration     ']
                st.write(branch_data)

            with row01_2:
                del_data = df.groupby(['Loan Officer', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                del_data = del_data[[
                    'Loan Officer', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(del_data)

            with row01_3:
                del_data = df.groupby(['Loan Officer', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                del_data = del_data[[
                    'Loan Officer', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                del_data = del_data[del_data['Delinquent Reason Descriptions']
                                    == 'National Emergency Declaration     ']
                st.write(del_data)

        row2_space1, row2_1, row2_space2, row2_2 = st.beta_columns(
            (.01, 1, .01, 1))
        if st.button('Display Stats'):

            with row2_1:
                stats = df.describe().transpose()
                stats = stats.drop(
                    ['Loan Number', 'Delinquent Reason'], axis=0)
                stats = stats.reset_index()
                st.write(stats)
            with row2_2:
                cat_stats = df.describe(
                    include=['object']).transpose().reset_index()
                st.write(cat_stats)

        """
        # Step 3: Choose Analysis
        """
        lo = list(df['Loan Officer'].unique())
        branch = list(df['Branch Name'].unique())
        processor = list(df['Loan Processor'].unique())
        underwriter = list(df['Underwriter'].unique())
        division = list(df['Division Name'].unique())
        company = list(df['Company'].unique())

        analysis = st.selectbox(
            'Choose Analysis', ['Company', 'Division', 'Branch Name', 'Loan Officer'])

        if analysis == 'Branch Name':
            st.subheader('** Branch Analysis**')
            line1_spacer1, line1_1, line1_spacer2 = st.beta_columns(
                (.1, 3.2, .1))
            selection = st.selectbox('Select Branch', branch)
            new_df = df[df['Branch Name'] == selection]

            row3_space1, row3_1, row3_space2, row3_2, row3_space3, row3_3 = st.beta_columns(
                (.01, 1, .01, 1, 0.01, 1))
            with row3_1:
                branch_lo_data = new_df.groupby(['Loan Officer', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_lo_data = branch_lo_data[[
                    'Loan Officer', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_lo_data)

            with row3_2:
                branch_underwriter_data = new_df.groupby(['Underwriter', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_underwriter_data = branch_underwriter_data[[
                    'Underwriter', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_underwriter_data)

            with row3_3:
                branch_processor_data = new_df.groupby(['Loan Processor', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_processor_data = branch_processor_data[[
                    'Loan Processor', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_processor_data)

            st.write(new_df)
            if st.button('Download Data'):
                if new_df is not None:
                    new_exp = new_df.to_csv(index=False)
                    # When no file name is given, pandas returns the CSV as a string, nice.
                    # some strings <-> bytes conversions necessary here
                    b64 = base64.b64encode(new_exp.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
                    st.markdown(href, unsafe_allow_html=True)

        if analysis == 'Loan Officer':
            st.subheader('** Loan Officer Analysis**')
            line1_spacer1, line1_1, line1_spacer2 = st.beta_columns(
                (.1, 3.2, .1))
            selection = st.selectbox('Select Loan Officer', lo)
            new_df = df[df['Loan Officer'] == selection]

            row3_space1, row3_1, row3_space2, row3_2, row3_space3, row3_3 = st.beta_columns(
                (.01, 1, .01, 1, 0.01, 1))
            with row3_1:
                lo_data = new_df.groupby(['Loan Officer', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                lo_data = lo_data[[
                    'Loan Officer', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(lo_data)

            with row3_2:
                branch_underwriter_data = new_df.groupby(['Underwriter', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_underwriter_data = branch_underwriter_data[[
                    'Underwriter', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_underwriter_data)

            with row3_3:
                branch_processor_data = new_df.groupby(['Loan Processor', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_processor_data = branch_processor_data[[
                    'Loan Processor', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_processor_data)

            st.write(new_df)
            if st.button('Download Data'):
                if new_df is not None:
                    new_exp = new_df.to_csv(index=False)
                    # When no file name is given, pandas returns the CSV as a string, nice.
                    # some strings <-> bytes conversions necessary here
                    b64 = base64.b64encode(new_exp.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
                    st.markdown(href, unsafe_allow_html=True)

        if analysis == 'Division':
            st.subheader('** Division Analysis**')
            row03_space1, row03_1 = st.beta_columns((.01, 1))
            with row03_1:
                all_divisions = df[['Division Name', 'Units']]
                all_divisions = all_divisions.groupby(
                    ['Division Name']).sum('Units').reset_index()
                st.write(all_divisions)
            line1_spacer1, line1_1, line1_spacer2 = st.beta_columns(
                (.1, 3.2, .1))
            selection = st.selectbox('Select Division', division)
            new_df = df[df['Division Name'] == selection]

            row3_space1, row3_1, row3_space2, row3_2, row3_space3, row3_3 = st.beta_columns(
                (.01, 1, .01, 1, 0.01, 1))
            with row3_1:
                lo_data = new_df.groupby(['Branch Name', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                lo_data = lo_data[[
                    'Branch Name', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(lo_data)

            with row3_2:
                branch_underwriter_data = new_df.groupby(['Underwriter', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_underwriter_data = branch_underwriter_data[[
                    'Underwriter', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_underwriter_data)

            with row3_3:
                branch_processor_data = new_df.groupby(['Loan Processor', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_processor_data = branch_processor_data[[
                    'Loan Processor', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_processor_data)

            st.write(new_df)
            if st.button('Download Data'):
                if new_df is not None:
                    new_exp = new_df.to_csv(index=False)
                    # When no file name is given, pandas returns the CSV as a string, nice.
                    # some strings <-> bytes conversions necessary here
                    b64 = base64.b64encode(new_exp.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
                    st.markdown(href, unsafe_allow_html=True)

        if analysis == 'Company':
            st.subheader('** Company Analysis**')
            row03_space1, row03_1 = st.beta_columns((.01, 1))
            with row03_1:
                all_divisions = df[['Company', 'Units']]
                all_divisions = all_divisions.groupby(
                    ['Company']).sum('Units').reset_index()

            line1_spacer1, line1_1, line1_spacer2 = st.beta_columns(
                (.1, 3.2, .1))
            selection = st.selectbox('Company Analysis', company)
            new_df = df[df['Company'] == selection]

            row3_space1, row3_1, row3_space2, row3_2, row3_space3, row3_3 = st.beta_columns(
                (.01, 1, .01, 1, 0.01, 1))
            with row3_1:
                lo_data = new_df.groupby(['Company', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                lo_data = lo_data[[
                    'Company', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(lo_data)

            with row3_2:
                branch_underwriter_data = new_df.groupby(['Branch Name', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_underwriter_data = branch_underwriter_data[[
                    'Branch Name', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_underwriter_data)

            with row3_3:
                branch_processor_data = new_df.groupby(['Loan Officer', 'Delinquent Reason Descriptions']).sum(
                    'Units').reset_index()
                branch_processor_data = branch_processor_data[[
                    'Loan Officer', 'Delinquent Reason Descriptions', 'Mortgage Amount', 'Units']]
                st.write(branch_processor_data)

            st.write(new_df)
            if st.button('Download Data'):
                if new_df is not None:
                    new_exp = new_df.to_csv(index=False)
                    # When no file name is given, pandas returns the CSV as a string, nice.
                    # some strings <-> bytes conversions necessary here
                    b64 = base64.b64encode(new_exp.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as ** &lt;file_name&gt;.csv**)'
                    st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
