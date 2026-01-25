import argparse
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from pathlib import Path
import joblib
import logging

from src.heart_disease.ml.dataset import load_data
from src.heart_disease.ml.model import HeartDiseaseClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train(
    data_path: str,
    epochs: int = 50,
    batch_size: int = 32,
    lr: float = 0.001,
    hidden_dim: int = 64,
    experiment_name: str = "Heart Disease Prediction"
):
    # Setup MLflow
    mlflow.set_experiment(experiment_name)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    with mlflow.start_run():
        # Log params
        mlflow.log_params({
            "epochs": epochs,
            "batch_size": batch_size,
            "learning_rate": lr,
            "hidden_dim": hidden_dim
        })
        
        # Load Data
        logger.info("Loading data...")
        train_dataset, val_dataset, preprocessor = load_data(data_path)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        # Save Preprocessor
        joblib.dump(preprocessor, "preprocessor.joblib")
        mlflow.log_artifact("preprocessor.joblib")
        
        # Initialize Model
        # Input dim is determined by processed data shape
        input_dim = train_dataset[0][0].shape[0]
        model = HeartDiseaseClassifier(input_dim=input_dim, hidden_dim=hidden_dim).to(device)
        
        criterion = nn.BCEWithLogitsLoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        
        # Training Loop
        logger.info("Starting training...")
        best_val_loss = float("inf")
        
        for epoch in range(epochs):
            model.train()
            train_loss = 0.0
            correct = 0
            total = 0
            
            for X, y in train_loader:
                X, y = X.to(device), y.to(device)
                
                optimizer.zero_grad()
                outputs = model(X)
                loss = criterion(outputs, y)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                predicted = (torch.sigmoid(outputs) > 0.5).float()
                total += y.size(0)
                correct += (predicted == y).sum().item()
            
            avg_train_loss = train_loss / len(train_loader)
            train_acc = correct / total
            
            # Validation
            model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for X, y in val_loader:
                    X, y = X.to(device), y.to(device)
                    outputs = model(X)
                    loss = criterion(outputs, y)
                    
                    val_loss += loss.item()
                    predicted = (torch.sigmoid(outputs) > 0.5).float()
                    val_total += y.size(0)
                    val_correct += (predicted == y).sum().item()
            
            avg_val_loss = val_loss / len(val_loader)
            val_acc = val_correct / val_total
            
            logger.info(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_train_loss:.4f} Acc: {train_acc:.4f} | Val Loss: {avg_val_loss:.4f} Acc: {val_acc:.4f}")
            
            mlflow.log_metrics({
                "train_loss": avg_train_loss,
                "train_acc": train_acc,
                "val_loss": avg_val_loss,
                "val_acc": val_acc
            }, step=epoch)
            
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                torch.save(model.state_dict(), "best_model.pth")
        
        # Log Best Model
        mlflow.log_artifact("best_model.pth")
        
        # Also log pyscript model for easy loading
        mlflow.pytorch.log_model(model, "model")
        
        logger.info("Training complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data/heart.csv")
    args = parser.parse_args()
    
    train(data_path=args.data_path)
