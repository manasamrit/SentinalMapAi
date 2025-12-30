# 🛡️ SentinelMap AI: Trust & Safety Investigation Console

**SentinelMap AI** is an advanced "Agentic AI" Proof of Concept designed to automate the detection of fraud, abuse, and deceptive behavior on Google Maps. It replicates the workflow of a human Trust & Safety Analyst but operates at the speed of code.

---

## 🚀 How to Run the App

### Prerequisites
*   Python 3.10+
*   API Keys (Optional for Demo Mode, required for Live Mode):
    *   Google Maps Platform (Places API)
    *   SerpApi (Google Search Results)
    *   Google Gemini API (Generative AI)

### Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/SentinelMapAi.git
    cd SentinelMapAi
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    python -m streamlit run app.py
    ```

4.  **Access the Dashboard**:
    Open your browser to `http://localhost:8501`.

---

## 🛠️ Tech Stack & Architecture

This project uses a **Modular Microservices Architecture** built entirely in Python.

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Rapid creation of the interactive "Command Center" dashboard and visualizations. |
| **LLM Engine** | Google Gemini 1.5 Flash | The "Brain" (Agent B) that reads policies and decides if a business is fraudulent. |
| **Data Layer** | Google Places API | Fetches "Ground Truth" data (Official Name, Address, Phone). |
| **OSINT Layer** | SerpApi | Searches the open web for "Digital Footprints" (YellowPages, Social Media). |
| **Risk Engine** | Python (Pandas/Plotly) | Deterministic logic to calculate the final 0-100 Trust Score. |

---

## 🧠 System Logic: How "Agentic AI" Investigates Fraud

If you are learning about Agentic AI or Trust & Safety, here is how the system actually "thinks." It doesn't just look for keywords; it follows a reasoning chain similar to a human detective.

### 1. The Trigger Phase
A user inputs a target queries (e.g., "Ace Locksmith"). The system first checks: *Does this even exist on the map?*

### 2. The Investigator Agent (Agent A)
*   **Role**: The "Feet on the Ground."
*   **Task**: It gathers raw evidence.
*   **Key Logic**: It performs a "Co-Location Check." If a business claims to be a huge corporate office but the address resolves to a residential house in the suburbs (via Zoning checks or visual context), Agent A flags this as suspicious.

### 3. The Policy Auditor Agent (Agent B)
*   **Role**: The "Judge."
*   **Task**: It reads the *Google Maps User Contributed Content Policy* and compares it against the evidence.
*   **Example Reasoning**:
    > "I see the business name is 'Best Fast Cheap Locksmith 24/7'. The policy forbids 'Keyword Stuffing'. Therefore, this is a violation of the Misrepresentation Policy."

### 4. The Review Integrity Module
*   **Role**: The "Mathematician."
*   **Task**: It plots review timestamps.
*   **Burst Detection**: If a business receives 5 five-star reviews within a 2-hour window, the math engine flags this as a "Review Bomb" or "Bot Farm" attack. Humans don't write reviews in clusters like that naturally.

---

## 🦠 Detectable Threat Vectors

SentinelMap is tuned to catch specific "Real-World Deception" patterns:

1.  **Ghost Businesses**: Listings created at fake addresses to generate leads.
    *   *Detection*: Address Verification + Lack of Web Footprint.
2.  **Lead-Gen Scams**: Names like "Plumber Near Me" instead of a real brand.
    *   *Detection*: Semantic analysis of the Name field.
3.  **Review Farms**: Fake engagement to boost ranking.
    *   *Detection*: Velocity Analysis (Time-series plotting).
4.  **VOIP/Burner Phones**: Using anonymous numbers to hide identity.
    *   *Detection*: Cross-referencing phone numbers with known business directories.

---

## ☁️ Deployment Guide

To share this app with others (e.g., stakeholders, interviewers), deploy it to the cloud.

### Option A: Streamlit Community Cloud (Easiest)
1.  Push this code to a public **GitHub Repository**.
2.  Go to [share.streamlit.io](https://share.streamlit.io).
3.  Connect your GitHub and select the repository.
4.  **Important**: In the "Advanced Settings," add your API keys as **Secrets**:
    ```toml
    GOOGLE_MAPS_API_KEY = "your_key"
    GEMINI_API_KEY = "your_key"
    SERPAPI_KEY = "your_key"
    ```
5.  Click **Deploy**.

### Option B: Docker / Cloud Run
1.  Create a `Dockerfile`:
    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    EXPOSE 8501
    CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
    ```
2.  Build and Run:
    ```bash
    docker build -t sentinel-map .
    docker run -p 8501:8501 sentinel-map
    ```
