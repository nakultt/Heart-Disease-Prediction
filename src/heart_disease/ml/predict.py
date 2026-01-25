import torch
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Union, Any

from src.heart_disease.ml.model import HeartDiseaseClassifier

class HeartDiseasePredictor:
    def __init__(self, model_path: str, preprocessor_path: str, device: str = "cpu"):
        self.device = torch.device(device)
        self.preprocessor = joblib.load(preprocessor_path)
        
        # Load Model
        # We need to know input_dim to instantiate the architecture
        # In a real scenario, this metadata should be saved with the model (e.g. in MLflow)
        # For now, we infer it from the preprocessor or hardcode based on known feature count.
        # The scaler + one-hot encoding expands features.
        # Let's assume we load a dummy batch to check or load metadata.
        # FIX: We will save the input_dim in the trainer as a simple file or attribute if possible.
        # ideally we load it from mlflow config. 
        # For this implementation, we will try to infer or use a reasonable default/argument.
        # Let's assume the user passes the dimension or we try to run a transform to check.
        
        # HACK: To get the dimension, we can inspect the transformer. 
        # But OneHotEncoder output depends on categories seen.
        # We will assume the preprocessor is fitted.
        # A robust way:
        try:
             # Try to get n_features_in_ or similar properties from the column transformer's transformers
             pass
        except:
             pass
             
        # Alternative: We used 64 hidden dim in trainer, but input dim is dynamic.
        # Let's just catch the exception on first forward pass or require explicit dim.
        # BETTER APPROACH: Save metadata.json in trainer.
        pass

    def load_model(self, model_path: str, input_dim: int, hidden_dim: int = 64):
        self.model = HeartDiseaseClassifier(input_dim=input_dim, hidden_dim=hidden_dim).to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def predict(self, input_data: Dict[str, Any]) -> float:
        """
        Args:
            input_data: Dict containing features like 'age', 'sex', etc.
        Returns:
            Probability of heart disease (0.0 to 1.0)
        """
        # Convert dict to DataFrame
        df = pd.DataFrame([input_data])
        
        # Preprocess
        X_processed = self.preprocessor.transform(df)
        if hasattr(X_processed, "toarray"):
            X_processed = X_processed.toarray()
            
        # Tensorize
        X_tensor = torch.tensor(X_processed, dtype=torch.float32).to(self.device)
        
        # Check if model is loaded; if not, we can't predict. 
        # We assume load_model was called. 
        # Note: We need input_dim to init model.
        if not hasattr(self, 'model'):
            # Lazy init if we didn't call load_model explicitly
            input_dim = X_tensor.shape[1]
            # Use default model path relative to preprocessor if not provided
            # This is a bit magic, but simplifies API usage
            pass 
            
        with torch.no_grad():
            logits = self.model(X_tensor)
            prob = torch.sigmoid(logits).item()
            
        return prob

# Helper to easy load
def get_predictor(model_dir: str = ".") -> HeartDiseasePredictor:
    # This assumes artifacts are in the current dir or specific dir
    preprocessor_path = Path(model_dir) / "preprocessor.joblib"
    model_path = Path(model_dir) / "best_model.pth"
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    predictor = HeartDiseasePredictor(str(model_path), str(preprocessor_path), device=device)
    
    # Init model with dummy transform to get shape
    # This is a safe way to determine input shape for the MLP
    # We create a dummy DF with 0s to check shape
    # But we need column names.
    # We can inspect preprocessor to get feature names? 
    # Or just use the model_state_dict to infer input layer weight shape.
    
    state_dict = torch.load(model_path, map_location="cpu")
    # layer_1.0.weight shape is (hidden, input)
    input_dim = state_dict["layer_1.0.weight"].shape[1]
    
    predictor.load_model(str(model_path), input_dim)
    
    return predictor
