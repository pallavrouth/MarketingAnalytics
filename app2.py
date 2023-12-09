import streamlit as st
import pandas as pd
import numpy as np
from plotnine import (
    ggplot,
    aes,
    geom_histogram,
    geom_bar,
    theme,
    theme_minimal,
    theme_bw,
    element_text,
    ylab,
    xlab
)
import statsmodels.api as sm

st.title(':blue[Customer Churn Behavior]')

with st.sidebar:
    st.markdown("# About")
    st.markdown(
            "This is my first python based web app."
            " The data depicts customer's churning behavior in a bank." 
            " It contains information how certain transaction specific factors and demographic factors impacts a customer's decision to churn."
            " I explore these factors in this app." 
            )
    st.markdown("")

tab1, tab2 = st.tabs(["Exploration","Modeling"])

with tab1:

    churn = (
        pd.read_csv('https://raw.githubusercontent.com/pallavrouth/MarketingAnalytics/main/datasets/churn.csv')
          .assign(has_card = lambda d: np.where(d.HasCrCard == 1,"Has credit card","No credit card"),
                  active = lambda d: np.where(d.IsActiveMember == 1,"Active","Inactive"),
                  Churn = lambda d: np.where(d.Exited == 1,"Churned","Not churned"))
          .assign(CustomerId = lambda d: d.CustomerId.apply(str),
                  Geography = lambda d: pd.Categorical(d.Geography),
                  Gender = lambda d: pd.Categorical(d.Gender),
                  has_card = lambda d: pd.Categorical(d.has_card),
                  active = lambda d: pd.Categorical(d.active),
                  Tenure = lambda d: pd.Categorical(d.Tenure, ordered = True),
                  PPurchase = lambda d: pd.Categorical(d.NumOfProducts, ordered = True))
          .drop(columns = ['RowNumber','Surname','HasCrCard','IsActiveMember','Exited','NumOfProducts'])
          .rename(columns = {'CreditScore':'Credit score',
                             'Geography':'Country of residence',
                             'Balance':'Bank balance to date',
                             'PPurchase':'Products purchased',
                             'EstimatedSalary':'Customer salary',
                             'has_card':'Credit card status',
                             'active':'Active status'
                             })
    )

    dataframe_container = st.container()
    st.markdown("**Select from the following columns to generate visualizations and statistics**")
    numerical_columns = ("Credit score","Age","Bank balance to date","Customer salary")
    categorical_columns = ("Gender","Products purchased","Tenure","Country of residence","Credit card status","Active status")
    column_input = st.radio("Columns", numerical_columns + categorical_columns, horizontal = True)
    plot_container = st.container()
    stats_container = st.container()

    with dataframe_container:
        st.markdown("**Data View**")
        st.dataframe(churn.head(n = 20), hide_index = True) 

    with plot_container:
        st.markdown("**Plot View**")
        if column_input in numerical_columns:
            plot = (
                ggplot(churn, aes(x = column_input)) + 
                    geom_histogram(bins = 25, color = "white", fill = "grey") + 
                    theme_bw() +
                    theme(axis_text = element_text(family = 'arial', color = "black"),
                            axis_title = element_text(family = 'arial', color = "black")) +
                    ylab("Count")
            )
            st.pyplot(ggplot.draw(plot))
        else:
            categories = len(churn[column_input].unique())
            if categories < 10:
                plot = (
                    ggplot(churn, aes(x = column_input)) + 
                        geom_bar(color = "white", fill = "grey") +
                        theme_bw() +
                        theme(axis_text = element_text(family = 'arial', color = "black"),
                                axis_title = element_text(family = 'arial', color = "black")) +
                        xlab(f"{column_input}") + 
                        ylab("Count")
                ) 
                st.pyplot(ggplot.draw(plot))
            else:
                st.markdown("Too many categories create visualization")

    with stats_container:
        st.markdown("**Stat View**")
        if column_input in numerical_columns: 
            stats_df = churn.describe().loc[:,[column_input]]
            st.dataframe(stats_df)
        else:
            unique_customers = len(churn.CustomerId.unique())
            counts_df = (
                churn
                    .groupby(column_input)
                    .agg(observations = ('CustomerId','nunique'))
                    .assign(proportion = lambda d: d.observations/unique_customers)
            ) 
            st.dataframe(counts_df)

with tab2:

    churn = (
        pd.read_csv('https://raw.githubusercontent.com/pallavrouth/MarketingAnalytics/main/datasets/churn.csv')
          .rename(columns = {'CreditScore':'Credit score',
                             'Geography':'Country of residence',
                             'Balance':'Bank balance to date',
                             'PPurchase':'Products purchased',
                             'EstimatedSalary':'Customer salary',
                             'HasCrCard':'Credit card status',
                             'IsActiveMember':'Active status',
                             'Exited':'Churn'
                             })
    )

    independent_variables = st.multiselect("Add variables",
                                           ["Credit score","Age","Bank balance to date","Customer salary","Gender",
                                           "Products purchased","Tenure","Country of residence","Credit card status",
                                           "Active status"],
                                           ["Credit score"])
    
    target = churn.loc[:,'Churn']
    features = churn.loc[:,independent_variables]

    X = sm.add_constant(features)
    logit_model = sm.Logit(target, X)
    model_sm = logit_model.fit()

    summary_table = pd.DataFrame({
        'coefficient': model_sm.params,
        'standard Error': model_sm.bse,
        'z-value': model_sm.tvalues,
        'p-value': model_sm.pvalues
    })
    st.dataframe(summary_table)

    def interpretations(summ_tab, var_name):
        filter_rows = summ_tab[summ_tab.index == var_name]
        effect = round(filter_rows['coefficient'][0],3)
        if effect < 0:
            return f"For one unit increase in **{var_name}** log-odds of churning decreases by {effect} units"
        else:
            return f"For one unit increase in **{var_name}** log-odds of churning decreases by {effect} units"


    response_container = st.container()
    with response_container:
        st.markdown("**Interpreting the coefficients**")
        for i, var in enumerate(features):
            st.markdown(f"{i+1}. {interpretations(summary_table, var)}")






        
            



