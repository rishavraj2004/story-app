# Story Generator App 📖✨

This is a **Story Generator Web Application** built using **Python Flask** that generates creative stories using the **Mistral API**.  
The application runs locally on `localhost` and securely uses an API key stored in an environment file that is excluded via `.gitignore`.

---

## 🚀 Features
- Generate AI-powered stories based on user input
- Built with Python Flask backend
- Uses Mistral AI for story generation
- Simple and clean web interface
- Secure API key handling using environment variables
- Runs locally on your system

---

## 🛠️ Tech Stack
- Python 3.x
- Flask
- Mistral API
- HTML / CSS
- python-dotenv

---

## 📂 Project Structure
Story-App/
│
├── app.py
├── templates/
│ └── index.html
├── static/
│ └── style.css
├── .gitignore
├── .env # Not committed
├── requirements.txt
└── README.md


---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/story-app.git
cd story-app
```
### 2️⃣ Create a Virtual Environment (Recommended)
```bash
python -m venv venv
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### If requirements.txt is not available:
```bash
pip install flask python-dotenv mistralai
```

### 4️⃣ Set Up Mistral API Key
Create a .env file in the root directory and add:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```
### 5️⃣ Run the Application
```
python app.py
```

### 6️⃣ Open in Browser
Open your browser and visit:
```
http://127.0.0.1:5000/
```


### 🧠 How It Works

User enters a prompt or story idea

Flask backend sends the prompt to the Mistral API

Mistral generates a story response

The generated story is displayed on the web page

###🤝 Contributions

Contributions are welcome!
Feel free to fork the repository and improve the project.

