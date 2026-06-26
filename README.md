# 🛡️ AI-Powered Phishing Guard
### Bridging Detection and Explainability using DistilBERT & Google Gemini

An AI-powered phishing email detection system that combines the speed of **DistilBERT** with the reasoning capabilities of **Google Gemini** to accurately classify phishing emails while providing human-readable explanations.

---

## 📌 Overview

Traditional phishing detection systems often classify emails as phishing or legitimate without explaining their decision. This project addresses that limitation by combining Machine Learning with Generative AI.

The application first classifies an email using a fine-tuned DistilBERT model and then uses Google Gemini to generate an explanation highlighting suspicious content, urgency tactics, malicious URLs, and social engineering indicators.

---

## ✨ Features

- AI-powered phishing email detection
- DistilBERT-based email classification
- Explainable AI using Google Gemini
- Human-readable threat analysis
- Real-time prediction
- User-friendly Gradio interface
- Confidence score for predictions

---

## 🏗️ System Architecture

```
User Email
     │
     ▼
Preprocessing
     │
     ▼
DistilBERT Classifier
     │
     ├────────► Legitimate
     │
     ▼
Google Gemini Analysis
     │
     ▼
Threat Explanation
     │
     ▼
Gradio Web Interface
```

---

## 🧠 Technologies Used

- Python
- DistilBERT
- Hugging Face Transformers
- Google Gemini API
- Gradio
- Scikit-learn
- Pandas
- NumPy
- Google Colab
- Jupyter Notebook

---

## 📂 Dataset

The model was trained using the **PhishingEmailDetection v2.0** dataset containing over **22,000 labeled email samples**.

Data preprocessing included:

- Removing duplicate records
- Removing empty emails
- Text normalization
- Binary label mapping
- 80/20 Train-Test split

---

## ⚙️ Working

1. User enters email text.
2. Email is preprocessed.
3. DistilBERT predicts whether the email is Legitimate or Phishing.
4. Google Gemini analyzes suspicious content.
5. A detailed explanation is generated.
6. Results are displayed in the Gradio interface.

---

## 📊 Model Highlights

- Fine-tuned DistilBERT model
- Binary Classification
- Explainable AI
- Near real-time prediction
- Human-readable security reasoning

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/phishing-guard.git
```

Move into the project

```bash
cd phishing-guard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create your environment file

```text
.env
```

Add your Gemini API Key

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Run the application

```bash
python app.py
```

---

## 📁 Project Structure

```
phishing-guard/
│
├── app.py
├── train_model.py
├── predict.py
├── model/
├── templates/
├── static/
├── dataset/
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example
```

---

## 🔮 Future Scope

- Browser extension for Chrome & Firefox
- Enterprise Email Security API
- Multi-language phishing detection
- URL reputation integration
- Continuous model retraining

---

## 👥 Team Members

- Shivansh Pandey
- Akansha Sen
- Ashika Bajpai

---

## 📄 License

This project is developed for educational and research purposes.

---

## ⭐ Acknowledgements

- Hugging Face
- Google Gemini
- Gradio
- Scikit-learn
- PhishingEmailDetection v2.0 Dataset