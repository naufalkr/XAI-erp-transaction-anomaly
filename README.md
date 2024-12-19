# ERP Anomaly Detection with Generative AI

## Description

This project aims to design and implement a cutting-edge solution that combines Generative AI, Explainable AI (XAI), and a Chatbot Assistant to detect anomalies in financial transactions. The system will identify suspicious activities with high accuracy while providing clear and actionable explanations for why specific transactions are flagged as anomalies. A chatbot will serve as an interactive interface, enabling users to query anomaly details and receive real-time explanations in an intuitive and user-friendly manner.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   ```
2. Navigate to the project directory:
   ```bash
   cd yourproject
   ```
3. Setup venv
   ```bash
   python -m venv /path/to/new/virtual/environment
   ```
4. Navigate to venv/scripts
   ```bash
   cd venv/scripts
   ```
5. Activate the Virtual Environment
   ```bash
   activate.bat
   ```
6. Install Python and Vite dependencies:

   - Server

   ```bash
   pip install -r requirements.txt
   ```

   - UI

   ```bash
   npm install
   ```

## Usage

1. Start the development ui server:
   ```bash
   npm run serve
   ```
2. Start the development python server:

   ```bash
    python3 -m flask --app ./model/app.py run
   ```
