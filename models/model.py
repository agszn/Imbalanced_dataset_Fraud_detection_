import xgboost as xgb

# Load the model in its current form
model = xgb.Booster(model_file='fraud_detection_model.pkl')

# Re-save the model using the latest version of XGBoost
model.save_model('fraud_detection_model.json')
