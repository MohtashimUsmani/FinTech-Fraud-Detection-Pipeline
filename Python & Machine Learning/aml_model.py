import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE  # <--- NEW: The Simulation Engine

# ---------------------------------------------------------
# 1. DATA EXTRACTION (The Pantry)
# ---------------------------------------------------------
print("Connecting to database and fetching data...")
engine = create_engine('postgresql://postgres:admin123@localhost:5432/fraud_detection')
query = "SELECT * FROM transactions LIMIT 1000000"

try:
    df = pd.read_sql(query, engine)
    print("\n--- Data Loaded Successfully ---")
    print(f"Total Rows: {len(df)}")
    print(f"Fraud Distribution:\n{df['isfraud'].value_counts()}")
except Exception as e:
    print(f"An error occurred: {e}")

# ---------------------------------------------------------
# 2. FEATURE ENGINEERING (The Lab)
# ---------------------------------------------------------
print("\nEngineering features...")
df['bal_error'] = (df['amount'] + df['oldbalancedest']) - df['newbalancedest']
df['is_zero_dest'] = ((df['oldbalancedest'] == 0) | (df['newbalancedest'] == 0)).astype(int)
df = pd.get_dummies(df, columns=['type'], prefix='type')

# Select features
features = ['amount', 'oldbalanceorg', 'newbalanceorig', 'bal_error', 'is_zero_dest']
type_cols = [col for col in df.columns if 'type_' in col]
X = df[features + type_cols]
y = df['isfraud']

# Split data: 80% Study Material (Train), 20% Final Exam (Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------------------------
# 3. SMOTE: HANDLING CLASS IMBALANCE (The Simulation)
# ---------------------------------------------------------
print("\n--- Applying SMOTE to Training Data ---")
print(f"Original Training Fraud Cases: {sum(y_train == 1)}")

# Generate synthetic fraud cases for the AI to study
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f"New Synthetic Training Fraud Cases: {sum(y_train_smote == 1)}")
print("SMOTE Complete. Training is now perfectly balanced.")

# ---------------------------------------------------------
# 4. MODEL TRAINING (The Brain)
# ---------------------------------------------------------
print("\nTraining the Random Forest model on balanced data...")
model = RandomForestClassifier(n_estimators=50, max_depth=10, n_jobs=-1, random_state=42)
# Notice we are training on the SMOTE data!
model.fit(X_train_smote, y_train_smote)

# ---------------------------------------------------------
# 5. EVALUATION & VISUALIZATION (The Cockpit)
# ---------------------------------------------------------
# We test on the REAL data (X_test), never the fake SMOTE data.
predictions = model.predict(X_test)
print("\n--- Model Performance Report (With SMOTE) ---")
print(classification_report(y_test, predictions))

# --- PLOT 1: The Red Confusion Matrix ---
cm = confusion_matrix(y_test, predictions)

plt.figure(figsize=(8, 6))
# Using 'Reds' so you know this is the SMOTE-enhanced version
sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',
            xticklabels=['Normal', 'Fraud'],
            yticklabels=['Normal', 'Fraud'])
plt.title('Fraud Detection Confusion Matrix (SMOTE Applied)')
plt.ylabel('Actual Transaction Label')
plt.xlabel('AI Predicted Label')
plt.show()

# --- PLOT 2: Feature Importance ---
importances = model.feature_importances_
feature_names = X.columns
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
importance_df = importance_df.sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=importance_df, palette='viridis')
plt.title('Which Features Drive Fraud Detection? (Post-SMOTE)')
plt.tight_layout()
plt.show()

print("\nPipeline execution finished. Check your SciView Plots!")

# ---------------------------------------------------------
# 6. EXPORTING TO POWER BI (The Business Report)
# ---------------------------------------------------------
print("\nPreparing data for Power BI Dashboard...")

# 1. Create a copy of your test data (so we don't mess up the original)
results_df = X_test.copy()

# 2. Add the actual truth from the bank
results_df['Actual_Fraud'] = y_test

# 3. Add the AI's predictions
results_df['AI_Predicted_Fraud'] = predictions

# 4. Optional: Calculate the financial impact (How much money was involved?)
# This is a great metric for Power BI!
results_df['Potential_Loss'] = results_df['amount']

# 5. Export to a CSV file
csv_filename = "fraud_predictions_for_powerbi.csv"
results_df.to_csv(csv_filename, index=False)

print(f"--- Success! Data exported to: {csv_filename} ---")