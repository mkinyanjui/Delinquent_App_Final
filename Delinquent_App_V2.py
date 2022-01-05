from matplotlib.figure import Figure
import base64
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import streamlit as st
st.set_page_config(layout='wide')


def main():

    st.title('Delinquent Exploration')

    """
    Created by Mark Kinyanjui

    """

    """
    # Import Data
    """
    df_imported = st.file_uploader(
        'Import dataset - data has already been cleaned and matched')

    if df_imported is not None:
        df = pd.read_excel(df_imported, sheet_name='Sheet1')

        df['Units'] = 1
        df['Company'] = 'AmCap'
        df['Decision'] = df['Delinquent Reason Descriptions'].apply(
            lambda x: 'National Emergency' if x == 'National Emergency Declaration     ' else 'Other')
        branch = pd.read_excel(df_imported, sheet_name='Branch')
        branch = branch.loc[branch['Status'] == 'Active']
        branch['Units'] = 1

        #lo = list(df['Loan Officer'].unique())
        branch_analysis = list(df['Branch Name'].unique())
        division = list(df['Division Name'].unique())
        #company = list(df['Company'].unique())
        """
        # FHA Overview
        """
        """
        This app  looks historically at FHA loans that have become delinquent
        within the last two years.
        """
        line1_spacer1, line1_1, line1_spacer2 = st.columns((.1, 3.2, .1))
        # status_selection = list(branch['Status'].unique())
        # selection = st.selectbox(
        #    'Active', status_selection)
        # status_df = branch[branch['Status'] == selection]
        # status_df = status_df[['Branch Name',
        #                       'Total Compare Ratio%', 'Total Orig', 'Total Seriously Delinquent', '% Seriously Delinquent and Claims']]

        row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.columns(
            (.1, 1, .1, 1, .1))
        with row1_1:
            st.subheader('Breakdown')
            fig = Figure()
            ax = fig.subplots()
            sns.countplot(x='Decision', data=df,
                          ax=ax, color='goldenrod')

            ax.set_xlabel('Delinquent Reason')
            ax.set_ylabel('Count')
            st.pyplot(fig)
            ned = df[df['Decision'] == 'National Emergency']
            ned = ned['Units'].sum()
            other = df[df['Decision'] != 'National Emergency']
            other = other['Units'].sum()

        with row1_2:
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown('')
            st.markdown(
                "There were **{}** units that fell under the **National Emergency Declaration**. Majority of these files may be due to COVID19. There were **{}** units that fell under **Other**. Reasons may include Unemployment, Excessive obligations, Curtailment of borrower income e.t.c. These are the potential problem files and should be looked up ".format(ned, other))

        """
        # Analysis
        """
        """
        This section lets you slice the data and look at it Division, Branch and loan detail level.
        """
        analysis = st.selectbox(
            'Division Analysis', ['Division'])

        division_count = df[['Division Name', 'Units']]
        division_count = division_count.groupby(
            'Division Name').sum().reset_index()
        division_prod = branch[['Division Name', 'Total Orig']]
        division_prod = division_prod.groupby(
            'Division Name').sum().reset_index()

        combined = pd.merge(division_prod, division_count,
                            how='left', on='Division Name')
        combined['Percentage'] = ((
            combined['Units'] / combined['Total Orig']) * 100).round(2)

        row01_1, row01_space2, row01_2 = st.columns(
            (1, .001, 1))
        with row01_1:
            fig, ax = plt.subplots()
            hbars = ax.bar(combined['Division Name'],
                           combined['Units'], align='center')
            # labels for bar plot data points
            xs = combined['Division Name']
            ys = combined['Units']
            for x, y in zip(xs, ys):
                label = "{:.0f}".format(y)
                plt.annotate(label, (x, y), textcoords="offset points",
                             xytext=(0, 1), ha='center')
            # labels end on the line above
            ax.set_ylabel('Total Units')
            st.pyplot(fig)
            '''
            The section above shows the breakdown of all FHA loans that became delinquent in each particular division within the past two years.

            '''
        with row01_2:
            fig, ax = plt.subplots()
            hbars = ax.bar(
                combined['Division Name'], combined['Percentage'], align='center')
            # labels for bar plot data points
            xs = combined['Division Name']
            ys = combined['Percentage']
            for x, y in zip(xs, ys):
                label = "{:.2f}%".format(y)
                plt.annotate(label, (x, y), textcoords="offset points",
                             xytext=(0, 1), ha='center')
            # labels end on the line above
            ax.set_ylabel('Percentage')
            st.pyplot(fig)
            '''
            The section above shows the percentage of loans that became delinquent based on the total FHA production within the past two years. Example: 20 files delinquent, 200 total FHA production equals a **10%** rate.

            '''

        if analysis == 'Company':
            line1_spacer1, line1_1, line1_spacer2 = st.columns(
                (.1, 3.2, .1))

        if analysis == 'Division':
            st.subheader('** Division Analysis**')

            selection = st.selectbox('Select Division', division)
            new_df = df[df['Division Name'] == selection]
            new_branchdf = branch[branch['Division Name'] == selection]

            st.subheader('Ratio')
            st.markdown(
                'The table below shows the FHA ratio. These values are provided by FHA. Click on any column title to sort by that column')
            branch_ratio = new_branchdf[[
                'Branch Name', 'Status', 'Total Compare Ratio%', 'Total Orig', 'Total Seriously Delinquent and Claims', '% Seriously Delinquent and Claims']]
            st.write(branch_ratio)
            st.write(
                'The table on the left shows you total units and loan amount that fell under the National Emergency Declaraction. The table on the right shows you all the files that were **NOT** under the National Emergency Declaration.')
            row1_1, row1_space2, row1_2 = st.columns(
                (1, .1, 1))
            with row1_1:
                st.markdown('**National Emergency Declaration Only**')
                branch_grouping_NED = new_df[new_df['Delinquent Reason Descriptions']
                                             == 'National Emergency Declaration     ']
                branch_grouping_NED = branch_grouping_NED[[
                    'Branch Name', 'Mortgage Amount', 'Units']]
                branch_grouping_NED = branch_grouping_NED.groupby(
                    'Branch Name').sum().reset_index()
                st.write(branch_grouping_NED)

            with row1_2:
                st.markdown('**All Other Reasons**')

                branch_grouping_NoNed = new_df[new_df['Delinquent Reason Descriptions']
                                               != 'National Emergency Declaration     ']
                branch_grouping_NoNed = branch_grouping_NoNed[[
                    'Branch Name', 'Mortgage Amount', 'Units']]
                branch_grouping_NoNed = branch_grouping_NoNed.groupby(
                    'Branch Name').sum().reset_index()
                st.write(branch_grouping_NoNed)

            st.markdown(
                'Select a Branch below to see the breakdown of the files that make up the ratio from above')
            branch_selection = st.selectbox('Select Branch', branch_analysis)
            branch_dataframe = df[df['Branch Name'] == branch_selection]
            branch_dataframe = branch_dataframe[['Loan Number', 'Borrower Name', 'Delinquent Reason Descriptions', 'Loan Officer', 'Loan Processor',
                                                 'Underwriter', 'Loan Purpose', 'Mortgage Amount', 'Interest Rate', 'Loan To Value Ratio', 'Credit Score', 'Oldest Unpaid Installment Due Date', 'Delinquent Status Date', 'Number of Months Delinquent']]
            new_df = branch_dataframe

            st.subheader('**Loan Details**')

            st.write(branch_dataframe)
            if st.button('Download Data'):
                if new_df is not None:
                    new_df = new_df.to_csv(index=False)
                    # When no file name is given, pandas returns the CSV as a string, nice.
                    # some strings <-> bytes conversions necessary here
                    b64 = base64.b64encode(new_df.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="Branch_data.csv">Download csv file</a>'


if __name__ == "__main__":
    main()
