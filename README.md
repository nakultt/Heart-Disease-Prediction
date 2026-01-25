# Heart Disease Prediction System (Enterprise Edition)

A full-stack machine learning application for predicting heart disease risk using Deep Learning (PyTorch), FastAPI, and React.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js & pnpm
- System Libraries: `torch` with CUDA support (optional but recommended)

### 2. Installation

**Backend**
```bash
# If using Poetry (Recommended)
poetry install

# If using pip/Conda manually
pip install torch torchvision mlflow pandas scikit-learn fastapi uvicorn pydantic-settings python-multipart numpy joblib
```

**Frontend**
```bash
cd frontend
pnpm install
```

### 3. Running the Project

You will need three terminal instances (or run in background):

#### Step 1: Train the Model (Run once)
This trains the PyTorch MLP model and saves `best_model.pth` and `preprocessor.joblib`.
```bash
# Using Python directly (if dependencies installed)
python -m src.heart_disease.ml.trainer

# OR using Poetry
poetry run python -m src.heart_disease.ml.trainer
```

#### Step 2: Start Backend API
Starts the FastAPI server at `http://localhost:8000`.
```bash
python -m src.heart_disease.main
# OR
uvicorn src.heart_disease.main:app --reload
```

#### Step 3: Start Frontend UI
Starts the Vite dev server at `http://localhost:5173`.
```bash
cd frontend
pnpm dev
```

## 🏗 Architecture
- **ML Engine**: `src/heart_disease/ml` (PyTorch, MLflow)
- **API**: `src/heart_disease/api` (FastAPI)
- **Frontend**: `frontend/` (React, TypeScript, Tailwind)
