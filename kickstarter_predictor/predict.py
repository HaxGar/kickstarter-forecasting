import kickstarter_predictor.registry

def pred(df, model_name) -> None:
    print('------Predict------')
    model = kickstarter_predictor.registry.load_model(model_name=model_name)
    model = model['model']
    X_live = df['X']
    y_pred = model.predict(X_live)[0]
    y_pred_proba = model.predict_proba(X_live)[0][y_pred]
    print(f"Predictions: {y_pred}")
    print(f"Prediction probabilities: {y_pred_proba}")
    return {'y_pred': y_pred,'y_pred_proba': y_pred_proba}
