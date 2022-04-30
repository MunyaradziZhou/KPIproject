from pycaret.regression import  *
import streamlit as st
import pandas as pd
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import plotly.express as px
import base64
import os
import io
from PIL import Image
import joblib
from pathlib import Path
#from utils.convert_dict_to_df import convert_dict_to_df




def app():
    state = st.file_uploader("Upload your input XLSX file", type=["xlsx"])

    if state is not None:
        
        df =  pd.read_excel(state,engine='openpyxl')
        dfs = st.dataframe(df)

        with st.expander("Traning and Testing Split"):
            file_name = st.text_input("Enter Model Name",value="")
            #n_select = st.number_input('Select To N Models',min_value=2,value=5)
            target_column = st.selectbox(
        'What would you like to predict?',df.columns.values.tolist(),)
            size = st.number_input('Training Size:', value=0.7)
            data_split_stratify = st.checkbox("Controls Stratification during Split", value=False)
            fold_strategy = st.selectbox('Choice of Cross Validation Strategy',options=['kfold','stratifiedkfold','groupkfold'])
            fold = st.number_input('Number of Folds to be Used in Cross Validation',min_value=2,value=10)
        # Processing 
        with st.expander("Preprocessing"):
            with st.container():
                st.markdown('<p style="color:#1386fc">Preprocessing for Numeric Columns:</p>',unsafe_allow_html=True)
                numeric_imputation = st.selectbox('Missing Value for Numeric Columns', options=['mean','median'])
                
                # select numberical features preprocessing
                normalize = st.checkbox('Normalization', value=False)
                normalize_method = 'zscore'
                if normalize:
                    normalize_method = st.selectbox('Method to be used for Normalization',options=['zscore','minmax','maxabs','robust'])
                
                transformation = st.checkbox('Transformation', value=False)
                transformation_method = 'yeo-johnson'
                if transformation:
                    transformation_method = st.selectbox('Method for Transfomation', options=['yeo-johnson','quantile'])
                
                fix_imbalance = st.checkbox('Fix Imbalance of Target Classes',value=False)
                # fix_imbalance_method = None
                # if fix_imbalance:
                #     fix_imbalance_method = st.selectbox('Method to Handle Imbalance', options=['SMOTE','fit_resample'])    
                #     if fix_imbalance_method == 'SMOTE':
                #         fix_imbalance_method = None

                # select categorical features
                categorical_columns = df.select_dtypes(include=['category','object']).columns.tolist()
                categorical_imputation = 'constant'
                unknown_categorical_method = 'least_frequent'
                combine_rare_levels = False
                rare_level_threshold = 0.1
                
                if len(categorical_columns) > 0:
                    st.markdown('<p style="color:#1386fc">Preprocessing for Categorical Columns:</p>',unsafe_allow_html=True)
                    with st.beta_container():
                        categorical_imputation = st.selectbox('Missing Values for Categorical', options=['constant','mode'])
                        unknown_categorical_method = st.selectbox('Handle Unknown Categorical values', options=['least_frequent','most_frequent'])
                        combine_rare_levels = st.checkbox('Combined Rare Levels of Categorical Features as a Single Level',value=False)
                        if combine_rare_levels:
                            rare_level_threshold = st.number_input('Percentile Distribution below Rare Categories are Combined',min_value=0.0,value=0.1)
        # Feature Engineering
        with st.expander("Creating New Features through Features Engineering"):
            with st.container():
                feature_interaction = st.checkbox('Create new Features by Interaction', value=False)
                feature_ratio = st.checkbox('Create new Features by Calculating Ratios', value=False)
                
                polynomial_features = st.checkbox('Create new Features based on Polynomial Combinations', value=False)
                polynomial_degree=2
                polynomial_threshold=0.1
                if polynomial_features:
                    polynomial_degree = st.number_input('Polynomial Degree (int)',min_value=1,step=1,value=2)
                    polynomial_threshold = st.number_input('Polynomial Threshold',min_value=0.0,value=0.1)
                
                trigonometry_features = st.checkbox('Create new Features based on all Trigonometric', value=False)                
                bin_numeric_features = st.checkbox('Create new Features based on Bin Combinations', value=False)
                select_bin_numeric_features=None
                
        with st.expander("Select Features in Dataset Contributes the most in Predicting Target Variable"):

            with st.container():
                feature_selection = st.checkbox('Select a Subset of Features Using a Combination of various Permutation Importance', value=False)
                feature_selection_threshold = 0.8
                if feature_selection:
                    feature_selection_threshold = st.number_input('Threshold for Feature Selection',min_value=0.0,value=0.8)
                    
                remove_multicollinearity = st.checkbox('Remove Highly Linearly Correlated Features', value=False)
                multicollinearity_threshold = 0.9
                if remove_multicollinearity:
                    multicollinearity_threshold = st.number_input('Threshold Used for Dropping the Correlated Features', min_value=0.0, value=0.9)
                
                remove_perfect_collinearity = st.checkbox('Remove Perfect Collinearity (Correaltion=1) Feature', value=False)
                
                pca = st.checkbox('Used PCA to Reduce the Dimensionality of the Dataset', value=False)
                pca_method='linear'
                pca_components = 0.99
                if pca:
                    pca_method = st.selectbox('The Method to Perform Linear Dimensionality Reduction', options=['linear','kernel','incremental'])
                    pca_components = st.number_input('Number of components to keep (float or int)', value=0.99)

                ignore_low_variance = st.checkbox('Remove Categorical Features with Statistically Insignificant Variances', value=False)
        
            sort = st.selectbox('The Sort Order of the Score Grid', options=['R2','MAE','MSE','RMSE','RMSLE','MAPE'], )
            fold_text = st.text_input('Control Cross Validation Folds (int or None)', value='None')
            fold_compare = None if fold_text == 'None' else int(fold_text)
            cross_validation = st.checkbox('Validation', value=True)

        if st.button("Train & Deploy"):


            setup(data=df, target=target_column,train_size=size, preprocess=True,
                    categorical_imputation=categorical_imputation, numeric_imputation=numeric_imputation,
                    normalize=normalize,normalize_method=normalize_method, transformation=transformation,
                    transformation_method=transformation_method, 
                    unknown_categorical_method=unknown_categorical_method,
                    combine_rare_levels=combine_rare_levels,rare_level_threshold=rare_level_threshold,
                    feature_interaction=feature_interaction,
                    feature_ratio=feature_ratio,polynomial_features=polynomial_features,
                    polynomial_degree=polynomial_degree,polynomial_threshold=polynomial_threshold,
                    trigonometry_features=trigonometry_features,
                    bin_numeric_features=select_bin_numeric_features,feature_selection=feature_selection,
                    feature_selection_threshold=feature_selection_threshold,remove_multicollinearity=remove_multicollinearity,
                    multicollinearity_threshold = multicollinearity_threshold,           
                    remove_perfect_collinearity=remove_perfect_collinearity, 
                    data_split_stratify=data_split_stratify,fold_strategy=fold_strategy,fold=fold,
                    pca=pca,pca_method=pca_method,pca_components=pca_components,
                    ignore_low_variance=ignore_low_variance,html=False,silent=True)
            
            log_history = {"setup":pull(True).data}
            
            best = compare_models(exclude=['xgboost'],fold=10, cross_validation=cross_validation, sort=sort)
            best_model_results = pull(best)
            st.table(best_model_results)
            #best_model_results.Model.tolist()

        

            is_finalize = st.checkbox("Model Finalized", value=True)
            if file_name:
                if is_finalize:
                    finalized_model = finalize_model(best)
                    _,name = save_model(finalized_model, file_name)
                    st.success('Model deployed successfuly')
                else:
                    _,name = save_model(best, file_name)
                    st.success('Model deployed successfuly')
            else:
                st.error("Please Give a File Name first!")

    
    
        


        
        

