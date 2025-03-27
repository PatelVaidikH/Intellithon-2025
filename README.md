# Intellithon-2025

## AI-Powered Supplier Search Agent

### 📌 Project Name: AI-Powered Supplier Search Agent
### 🏆 Team Name: AI Bots

#### 🔍 Solution Overview:
Our AI-powered search agent acts like **ChatGPT for suppliers and manufacturers**—helping businesses find, evaluate, and connect with the right industry partners through a **conversational AI interface**.

#### 🚀 Key Features:
✅ **Conversational AI Interface** – Users enter sourcing queries, and our AI finds suppliers instantly.  
✅ **Web Scraping & Data Extraction** – Extracts supplier data from **directories, websites, and trade portals** (e.g., IndiaMART, MFG.com).  
✅ **Automated Industry Classification** – Categorizes suppliers based on **capabilities, industries, and locations**.  
✅ **AI-Based Supplier Ranking** – Scores suppliers based on **credibility, relevance, and completeness of data**.  
✅ **Real-Time Monitoring** – Automates data updates to keep supplier details fresh and accurate.  
✅ **Search & Filtering** – Allows users to **search by location, industry, and certifications** for better results.  

#### 🎯 Impact:
Our solution revolutionizes industrial sourcing by **reducing manual research time and improving supplier discovery accuracy.**

#### 🎥 Demo Video:
https://github.com/user-attachments/assets/fcc7825f-c725-404f-b6e2-356d081636e6


---

### 📂 Project Structure:

#### **Backend (Flask API & Database Integration)**
- `integration/app.py` - Flask-based API to process supplier searches.
- `list.py` - Fetches unique locations & capabilities from the database.
- `clean.py` - Cleans and standardizes supplier location data.

#### **Web Scraping Modules (Data Collection)**
- `Web Scrapping/indiamart_scrapping.py` - Scrapes supplier data from IndiaMART.
- `Web Scrapping/mfg_automated_scrapping.py` - Scrapes suppliers from MFG.com for 5 continents and any capabilities.
- `Web Scrapping/gujaratdirectory_automated_scrapping.py` - Scrapes supplier details from Gujarat Directory.

#### **Frontend (User Interface for Supplier Search)**
- `integration/index.html` - Dashboard for supplier search and results.

#### **Database Setup**
- A MySQL database (`intellithon2025`) containing supplier details.

---

### 🛠 Instructions for Running the Project

#### **1️⃣ Install Dependencies:**
```bash
pip install flask flask-cors mysql-connector-python selenium requests beautifulsoup4 pandas openpyxl
```

#### **2️⃣ Set Up Database:**
- Import supplier data into `intellithon2025` MySQL database.

#### **3️⃣ Run the Flask API:**
```bash
python app.py
```

#### **4️⃣ Open `index.html` in a browser**
- Enter search queries to find suppliers.

---

### 🙏 Acknowledgments
A huge thank you to **MESH Works**, **Navrachana University**, and **Sahil Shah (CEO, MESH Works)** for organizing this incredible event and providing us the opportunity to build and showcase our AI-powered solution. Your vision for AI-driven business innovation has truly inspired us! 🚀🔥

---
