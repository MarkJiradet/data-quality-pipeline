# 🧹 Data Quality Pipeline for E-commerce

This project simulates and detects data quality issues in synthetic e-commerce transaction data.

## 🔧 Tech Stack
- Python / Streamlit
- DuckDB (in-memory analytics database)
- Docker (for deployment)

## 🚀 How to Run

### Option 1: Using Docker (Recommended)

```bash
docker build -t dq-pipeline .
docker run -p 8501:8501 dq-pipeline

Visit: http://localhost:8501

## Output
![Sample_output1](https://github.com/user-attachments/assets/0be40aad-684c-463d-9854-578486c4e07a)
