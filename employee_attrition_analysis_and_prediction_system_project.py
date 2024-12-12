# -*- coding: utf-8 -*-
"""Employee Attrition Analysis and Prediction System_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/132ROqIun9E6UodPKXisHyhNUNYbIkSVB

# Employee Attrition Analysis and Prediction System
Employee Attrition Analysis and Prediction, aimed at analyzing factors influencing employee attrition, predicting potential attrition, and providing actionable insights for HR teams to improve employee retention.

Acme Corporation, a leading tech company, is facing a significant challenge with employee turnover. The HR department is concerned about the increasing rate of attrition, as it negatively impacts team dynamics, project continuity, and overall company morale. To address this issue, Acme Corporation wants to leverage data analytics and machine learning to understand the factors influencing employee turnover and predict which employees are likely to leave in the near future.

---

# 1. Data Understanding and Exploration
Acme Corporation has provided historical data on employee demographics, job satisfaction, work environment, performance metrics, and turnover status. This dataset spans the last five years and includes information on employees who have left the company and those who are still currently employed.

```
# This is formatted as code
```
Load and explore the dataset, checking for data completeness and structure.

Verify dataset columns, data types, and check for missing values.

Understand the target variable (Attrition) and its distribution
"""

pip install imbalanced-learn

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
df=pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
df

data1=df
data1

df['Attrition']

df.head()

df.info()

df.describe()

#checking missing value
df.isnull().sum()

target_distribution=df['Attrition'].value_counts()
target_distribution

#Plot the target_distribution
import matplotlib.pyplot as plt
target_distribution.plot(kind='bar',title='Attrition Distribution')

plt.xlabel('Attrition')
plt.ylabel('Count')



"""**Task** 1.2: Perform univariate and bivariate analysis.

Visualize categorical variables (e.g., Department, Job Role, etc.) with attrition.

Analyze numerical features (e.g., Age, Monthly Income) for patterns.

Explore correlations between features using heatmaps or pair plots.
"""

import seaborn as sns

sns.countplot(data=df,x='Department',hue='Attrition')
plt.title('Department vs Attrition')

categorical_cols=df.select_dtypes(include=['object']).columns
categorical_cols

categorical_cols1=['Attrition', 'BusinessTravel', 'Department', 'EducationField', 'Gender']
categorical_cols2=['JobRole', 'MaritalStatus', 'Over18', 'OverTime']



fig,axes=plt.subplots(1,len(categorical_cols1),figsize=(15,6),sharey=True)

for i,col in enumerate(categorical_cols1):

    sns.countplot(data=df,x=col,hue='Attrition',ax=axes[i])
    axes[i].set_title(f'{col} vs Attrition')
    axes[i].tick_params(axis='x', rotation=45)


plt.tight_layout()
plt.show()

fig,axes=plt.subplots(1,len(categorical_cols2),figsize=(15,6),sharey=True)

for i,col in enumerate(categorical_cols2):

    sns.countplot(data=df,x=col,hue='Attrition',ax=axes[i])
    axes[i].set_title(f'{col} vs Attrition')
    axes[i].tick_params(axis='x', rotation=45)


plt.tight_layout()
plt.show()

#Numerical columns distributions
df.select_dtypes(include=['float64','int64']).columns

education_dist=df['Education'].value_counts()

education_dist.plot(kind='bar',title='Education Distribution')

plt.xlabel('Attrition')
plt.ylabel('Count')

sns.barplot(data=df,x='Education',y='MonthlyIncome',hue='Attrition')

numerical_cols = ['Age', 'MonthlyIncome', 'TotalWorkingYears', 'YearsAtCompany', 'YearsInCurrentRole']

# Plotting distributions of numerical variables grouped by 'Attrition'
for col in numerical_cols:
    plt.figure(figsize=(4, 3))
    sns.boxplot(x='Attrition', y=col, data=df)
    plt.title(f'{col} by Attrition')
    plt.show()

#Correlation heatmap
corr_matrix=df[numerical_cols].corr()
corr_matrix

plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix,annot=True,cmap='coolwarm',fmt='.2f')
plt.title('Correlation Heatmap')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(6,5))
sns.pairplot(vars=df[numerical_cols],data=df,hue='Attrition')
plt.suptitle('Pairplot of Numerical Features by Attrition', y=1.02)
plt.show()



"""## 2.Data Cleaning and Preprocessing
-Handle missing values.

Use mean/median imputation for numerical features.

Use mode/most frequent category imputation for categorical features.

-Encode categorical variables.

Use one-hot encoding or label encoding as appropriate for features like Department, Job Role, etc.

-Feature scaling.

Scale numerical features using Min-Max Scaling or Standard Scaling.

Task 2.4: Address class imbalance in the target variable.

Use techniques like SMOTE (Synthetic Minority Over-sampling Technique) or class weighting in models.
"""

#Handle missing values
df.isnull().sum()

#Encode Categorical Variables
df.select_dtypes(include=['object']).columns

non_ordinal_col=['Attrition','BusinessTravel','Department','EducationField','Gender','JobRole','MaritalStatus','Over18','OverTime']
df=pd.get_dummies(df,columns=non_ordinal_col,drop_first=True)
df

#convert True =1 ,False=0

boolean_cols=df.select_dtypes(include=['bool']).columns
df[boolean_cols]=df[boolean_cols].astype(int)
df

"""### Feature Engineering"""

df['TenureRatio'] = df['YearsAtCompany'] / (df['TotalWorkingYears'] + 1e-6)
df['JobIncomeInteraction'] = df['JobLevel'] * df['MonthlyIncome']

df[['JobIncomeInteraction','TenureRatio']]

#Feature Scaling
import sklearn
from sklearn.preprocessing import MinMaxScaler
df_numericals=df.select_dtypes(include=['float64','int64'])
df_numericals

scalar=MinMaxScaler()
df_scaled=scalar.fit_transform(df_numericals)
df_scaled_df=pd.DataFrame(df_scaled,columns=df_numericals.columns)
df_scaled_df

#SMOTE
df_scaled_df.head()

y=df_scaled_df['Attrition_Yes']
X=df_scaled_df.drop('Attrition_Yes',axis=1)

#split train-test part
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
smote=SMOTE(sampling_strategy='auto',random_state=42)
X_train_smote,y_train_smote=smote.fit_resample(X_train,y_train)

print("Class distribution in original training data:")
print(y_train.value_counts())

print("\nClass distribution after applying SMOTE:")
print(y_train_smote.value_counts())

y

df_scaled_df.head()

"""# 3.Feature Engineering
Generate new features.

Calculate tenure ratios (e.g., YearsAtCompany / TotalWorkingYears).

Interaction terms (e.g., JobLevel * MonthlyIncome).

Perform feature selection.

Use methods like Recursive Feature Elimination (RFE) or Feature Importance from Random Forest.
"""

#After completed Feature Engineering
df_scaled_df.head()

#Recursive Feature Elimination (RFE)
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

base_model=RandomForestClassifier(random_state=42)
rfe=RFE(estimator=base_model,n_features_to_select=5)
X_train_rfe=rfe.fit(X_train_smote,y_train_smote)
selected_features=X_train_rfe.get_support()
selected_features_names=X_train_rfe.feature_names_in_[selected_features]
selected_features_names

X_train_rfe

X_train_smote.columns[selected_features]

X_train_smote[X_train_smote.columns[selected_features]]

"""# 4.Model Building
Train initial models using different algorithms.

Logistic Regression, Decision Tree, Random Forest, XGBoost.

Evaluate models using cross-validation.

Metrics to use: Accuracy, Precision, Recall, F1 Score, ROC-AUC.
"""

X_train_smote_rfe=X_train_smote[X_train_smote.columns[selected_features]]
X_test_rfe=X_test[X_test.columns[selected_features]]

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score,cross_validate
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score

"""### LogisticRegression"""

log_reg=LogisticRegression(random_state=42)

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
cv_results = cross_validate(log_reg, X_train_smote_rfe, y_train_smote, cv=5, scoring=scoring)


print(f"Accuracy: {cv_results['test_accuracy'].mean():.4f}")
print(f"Precision: {cv_results['test_precision'].mean():.4f}")
print(f"Recall: {cv_results['test_recall'].mean():.4f}")
print(f"F1 Score: {cv_results['test_f1'].mean():.4f}")
print(f"ROC AUC: {cv_results['test_roc_auc'].mean():.4f}")

log_reg.fit(X_train_smote_rfe,y_train_smote)
y_pred=log_reg.predict(X_test_rfe)
accuracy=accuracy_score(y_test,y_pred)
precision=precision_score(y_test,y_pred)
recall=recall_score(y_test,y_pred)
f1=f1_score(y_test,y_pred)
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

"""### DecisionTreeClassifier"""

dec_tree=DecisionTreeClassifier(random_state=42)

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
cv_results = cross_validate(dec_tree, X_train_smote_rfe, y_train_smote, cv=5, scoring=scoring)


print(f"Accuracy: {cv_results['test_accuracy'].mean():.4f}")
print(f"Precision: {cv_results['test_precision'].mean():.4f}")
print(f"Recall: {cv_results['test_recall'].mean():.4f}")
print(f"F1 Score: {cv_results['test_f1'].mean():.4f}")
print(f"ROC AUC: {cv_results['test_roc_auc'].mean():.4f}")

"""### RandomForestClassifier"""

randm_class=RandomForestClassifier(random_state=42)

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
cv_results = cross_validate(randm_class, X_train_smote_rfe, y_train_smote, cv=5, scoring=scoring)


print(f"Accuracy: {cv_results['test_accuracy'].mean():.4f}")
print(f"Precision: {cv_results['test_precision'].mean():.4f}")
print(f"Recall: {cv_results['test_recall'].mean():.4f}")
print(f"F1 Score: {cv_results['test_f1'].mean():.4f}")
print(f"ROC AUC: {cv_results['test_roc_auc'].mean():.4f}")

"""### XGBClassifier"""

xgb_class=XGBClassifier(random_state=42)

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
cv_results = cross_validate(xgb_class, X_train_smote_rfe, y_train_smote, cv=5, scoring=scoring)


print(f"Accuracy: {cv_results['test_accuracy'].mean():.4f}")
print(f"Precision: {cv_results['test_precision'].mean():.4f}")
print(f"Recall: {cv_results['test_recall'].mean():.4f}")
print(f"F1 Score: {cv_results['test_f1'].mean():.4f}")
print(f"ROC AUC: {cv_results['test_roc_auc'].mean():.4f}")

"""### 5. Hyperparameter Tuning
Perform hyperparameter optimization using Grid Search or Random Search.

Use advanced optimization methods like Bayesian Optimization (optional).
"""

#XGBClassifier
from sklearn.model_selection import RandomizedSearchCV
xgb_model_hp=XGBClassifier(random_state=42,eval_metric='logloss')

param_dict={
    'n_estimators': np.arange(50, 300, 50),
    'max_depth': np.arange(3, 10),
    'learning_rate': np.linspace(0.01, 0.3, 10),
    'subsample': np.linspace(0.5, 1.0, 5),
    'colsample_bytree': np.linspace(0.5, 1.0, 5)

}

random_search = RandomizedSearchCV(estimator=xgb_model_hp,

            param_distributions=param_dict,
            n_iter=30, cv=5,
            scoring={'roc_auc': 'roc_auc', 'accuracy': 'accuracy'},
                                    refit='accuracy',
     random_state=42,verbose=0,n_jobs=1)

random_search.fit(X_train_smote_rfe, y_train_smote)

best_params = random_search.best_params_
print("Best Hyperparameters:", best_params)
print("Best accuracy:", random_search.best_score_)

best_model_xgb_hp=random_search.best_estimator_

from sklearn.metrics import roc_auc_score
y_test_pred = best_model_xgb_hp.predict_proba(X_test_rfe)[:, 1]
y_test_pred1 = best_model_xgb_hp.predict(X_test_rfe)
print("Test ROC-AUC Score:", roc_auc_score(y_test, y_test_pred),"accuracy ",accuracy_score(y_test,y_test_pred1))
print("\nClassification Report:")
print(classification_report(y_test, y_test_pred1))

y_test_pred1

#RandomForest
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report

rf_model = RandomForestClassifier(random_state=42)


param_dist = {
    'n_estimators': [100, 200, 300, 400, 500],
    'max_depth': [None, 10, 20, 30, 40],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

random_search_rf = RandomizedSearchCV(
    estimator=rf_model,
    param_distributions=param_dist,
    n_iter=50,
    cv=5,
    scoring='accuracy',
    random_state=42,
    verbose=1,
    n_jobs=-1
)


random_search_rf.fit(X_train_smote_rfe, y_train_smote)

print("Best Parameters:", random_search_rf.best_params_)
print("Best Score:", random_search_rf.best_score_)

best_rf_model = random_search_rf.best_estimator_
y_pred_rf = best_rf_model.predict(X_test_rfe)

print("\nClassification Report:")
print(classification_report(y_test, y_pred_rf))



"""### 6.Model Evaluation and Insights
Interpret model results.

Analyze feature importance to determine factors most influencing attrition.

Generate SHAP values for feature impact explanations.

Test model performance on a hold-out test dataset.
"""

#1 Using Random Forest Feature Importance
importances = best_model_xgb_hp.feature_importances_
feature_names = X_train_smote_rfe.columns
feature_importance_df=pd.DataFrame({'Feature':feature_names,'Importance':importances})
feature_importance_df=feature_importance_df.sort_values(by='Importance',ascending=False)
feature_importance_df

#2. SHAP (SHapley Additive exPlanations)

pip install shap

import shap
explainer= shap.TreeExplainer(best_model_xgb_hp)
shap_values=explainer.shap_values(X_test_rfe)
shap.summary_plot(shap_values, X_test_rfe)

shap_values=explainer.shap_values(X_train_smote_rfe)
shap.summary_plot(shap_values,X_train_smote_rfe)



"""## Machine Learning  Model Production"""



data=[[23,34,55,0,0]]
new_df = pd.DataFrame(data, columns=['MonthlyIncome', 'StockOptionLevel', 'YearsWithCurrManager',
       'OverTime_Yes', 'JobIncomeInteraction'])


single = best_model_xgb_hp.predict(new_df)
proba = best_model_xgb_hp.predict_proba(new_df)[:, 1]

if single == 1:
        output1 = "The Attrition"
        # Access the first element of the proba array using proba[0]
        output2 = "Confidence: {:.2f}%".format(proba[0] * 100)
else:
        output1 = "The Not Attrition"
        # Access the first element of the proba array using proba[0]
        output2 = "Confidence: {:.2f}%".format(proba[0] * 100)

#pkl model

model_last=best_model_xgb_hp
import pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(model_last, file)

#scaler.pkl
scaler=scalar
import pickle
with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

