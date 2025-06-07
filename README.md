# 🔐 Phishing URL Detection using Machine Learning

An end-to-end ML pipeline to detect phishing websites based on various URL features. The system is modular, production-ready, and deployed using **FastAPI**, **Docker**, **GitHub Actions**, and **AWS EC2**.

---

## 📂 Project Structure

```
Network_Security/
│
├── config/                  # Configuration files and schema
├── components/              # Core modules (ingestion, validation, transformation, training)
├── pipeline/                # Training and prediction pipelines
├── exception/               # Custom exception classes
├── logging/                 # Logging module
├── utils/                   # Utility/helper functions
├── app/                     # FastAPI web app
│   └── templates/           # HTML UI templates
│
├── artifacts/               # Stores processed data, artifacts
├── saved_models/            # Serialized trained models
├── .github/workflows/       # GitHub Actions CI/CD workflows
├── Dockerfile               # Docker build configuration
├── requirements.txt         # Project dependencies
├── .env                     # MongoDB credentials and other env variables
├── main.py                  # Entry point to run the pipeline
```

---

## 📊 Dataset Information

- Label: `Result`
  - `1`: Legitimate
  - `-1`: Phishing

- Example features:
  - `having_IP_Address`, `URL_Length`, `SSLfinal_State`, `Abnormal_URL`, `Google_Index`, etc.
  - Binary and integer values only (mostly -1, 0, 1)

---

## ⚙️ ML Pipeline Components

### 1. 📥 Data Ingestion
- Connects to MongoDB
- Downloads raw data
- Stores it in the `artifacts/raw.csv`

### 2. ✅ Data Validation
- Validates schema and data types
- Checks for nulls, data consistency
- Logs validation results

### 3. 🔄 Data Transformation
- Feature engineering
- Normalization/Scaling
- Converts to NumPy arrays

### 4. 🤖 Model Training
- Trains models (e.g. XGBoost, RandomForest)
- Evaluates performance using AUC, accuracy
- Saves the best model to `saved_models/`

### 5. 🌐 FastAPI Deployment
- UI for manual feature input
- REST API endpoint (`/predict`)
- JSON-based prediction response

---

## 🐳 Docker & CI/CD

### 🐳 Docker
- Containerizes the FastAPI app
- Ensures consistent runtime across environments

```bash
# Build the Docker image
docker build -t phishing-detector .

# Run the container
docker run -p 8000:8000 phishing-detector
```

### ⚙️ GitHub Actions
- Auto-deploys on push to `main`
- Pipeline includes:
  - ✅ Code Linting
  - 🧪 Unit Testing
  - 🐳 Docker Build
  - 🚀 Push to EC2

---

## ☁️ AWS EC2 Deployment

- Hosted on EC2 Ubuntu instance
- Docker used to run FastAPI server
- Port `8000` opened in security group
- Accessible via `http://<EC2-Public-IP>:8000`

---

## 💻 How to Run Locally

### 🧱 Setup

```bash
git clone https://github.com/Jana2207/Network_security.git
cd Network_security
```

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

### 🔐 Configure Environment

Create a `.env` file with:

```env
MONGO_DB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/
```

### ▶️ Run Pipeline

```bash
python main.py
```

### 🚀 Launch FastAPI App

```bash
cd app
uvicorn main:app --reload
```

---

## 🧠 Tech Stack

| Layer            | Tools/Frameworks                    |
|------------------|-------------------------------------|
| Language         | Python                              |
| Data Storage     | MongoDB                             |
| ML Libraries     | Scikit-learn, XGBoost               |
| API & UI         | FastAPI, HTML/CSS                   |
| CI/CD            | GitHub Actions                      |
| Containerization | Docker                              |
| Deployment       | AWS EC2                             |

---

## 🚀 Future Enhancements

- Add **MLFlow** for experiment tracking
- Introduce **feature extraction from raw URLs**
- Add **unit and integration tests**
- Enhance UI with auto-parsing from URL input

---

## 🙋‍♂️ Author

**Janardhan Reddy Illuru**  
📧 [LinkedIn](https://www.linkedin.com/in/janardhan-reddy-illuru)  
📨 jana2207@gmail.com



