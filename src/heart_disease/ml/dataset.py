import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import joblib
from pathlib import Path
from typing import Tuple, Optional

class HeartDiseaseDataset(Dataset):
    def __init__(self, csv_path: str, mode: str = "train", split_ratio: float = 0.8, random_seed: int = 42):
        """
        Custom PyTorch Dataset for Heart Disease Data.
        
        Args:
            csv_path: Path to the heart.csv file.
            mode: 'train' or 'val'.
            split_ratio: Ratio for training data.
            random_seed: Seed for reproducibility.
        """
        self.csv_path = csv_path
        self.mode = mode
        
        # Load Data
        df = pd.read_csv(csv_path)
        
        # Define Features
        # Define Features
        self.numeric_features = ["Age"]
        self.categorical_features = [
            "Chest_Pain", "Shortness_of_Breath", "Fatigue", "Palpitations", 
            "Dizziness", "Swelling", "Pain_Arms_Jaw_Back", "Cold_Sweats_Nausea", 
            "High_BP", "High_Cholesterol", "Diabetes", "Smoking", "Obesity", 
            "Sedentary_Lifestyle", "Family_History", "Chronic_Stress", "Gender"
        ]
        self.target_column = "Heart_Risk"
        
        # Split Data
        train_df = df.sample(frac=split_ratio, random_state=random_seed)
        val_df = df.drop(train_df.index)
        
        if mode == "train":
            self.data = train_df
            self.fit_preprocessor(train_df)
        else:
            self.data = val_df
            # For validation, we load the preprocessor fitted on training data
            # IN REAL PROD: This should be loaded from a file. 
            # HERE: We will refit for simplicity of independent instantiation, 
            # BUT ideally, the preprocessor should be passed in.
            # To fix this properly for this demo: Trainer should handle preprocessing logic and pass tensors/arrays.
            # However, to keep it self-contained:
            pass # Preprocessing handled externally or via shared state in a real pipeline
            
    def fit_preprocessor(self, df: pd.DataFrame):
        self.preprocessor = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), self.numeric_features),
                ("cat", OneHotEncoder(handle_unknown="ignore"), self.categorical_features),
            ]
        )
        self.preprocessor.fit(df.drop(columns=[self.target_column]))
        
    def transform(self, df: pd.DataFrame) -> Tuple[torch.Tensor, torch.Tensor]:
        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]
        
        X_processed = self.preprocessor.transform(X)
        if hasattr(X_processed, "toarray"):
            X_processed = X_processed.toarray()
            
        return torch.tensor(X_processed, dtype=torch.float32), torch.tensor(y.values, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # Note: This is inefficient for real-time training (transforming per item). 
        # Better to transform entire dataset in __init__.
        # For small datasets like this (300 rows), we can pre-process in __init__.
        pass

class ProcessedHeartDataset(Dataset):
    """
    More efficient version that processes everything upfront.
    """
    def __init__(self, X: np.ndarray, y: np.ndarray):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
        
    def __len__(self):
        return len(self.X)
        
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

def load_data(csv_path: str, test_size: float = 0.2, random_state: int = 42) -> Tuple[Dataset, Dataset, ColumnTransformer]:
    """
    Loads data, fits preprocessor on train, and returns Train/Val Datasets.
    """
    df = pd.read_csv(csv_path)
    
    numeric_features = ["Age"]
    categorical_features = [
        "Chest_Pain", "Shortness_of_Breath", "Fatigue", "Palpitations", 
        "Dizziness", "Swelling", "Pain_Arms_Jaw_Back", "Cold_Sweats_Nausea", 
        "High_BP", "High_Cholesterol", "Diabetes", "Smoking", "Obesity", 
        "Sedentary_Lifestyle", "Family_History", "Chronic_Stress", "Gender"
    ]
    target_column = "Heart_Risk"
    
    # Validation split
    train_df = df.sample(frac=1-test_size, random_state=random_state)
    val_df = df.drop(train_df.index)
    
    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )
    
    # Fit on Train
    X_train = train_df.drop(columns=[target_column])
    y_train = train_df[target_column].values
    
    preprocessor.fit(X_train)
    X_train_processed = preprocessor.transform(X_train)
    
    # Transform Val
    X_val = val_df.drop(columns=[target_column])
    y_val = val_df[target_column].values
    X_val_processed = preprocessor.transform(X_val)
    
    # Handle sparse output
    if hasattr(X_train_processed, "toarray"):
        X_train_processed = X_train_processed.toarray()
    if hasattr(X_val_processed, "toarray"):
        X_val_processed = X_val_processed.toarray()
        
    train_dataset = ProcessedHeartDataset(X_train_processed, y_train)
    val_dataset = ProcessedHeartDataset(X_val_processed, y_val)
    
    return train_dataset, val_dataset, preprocessor
