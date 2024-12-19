# ERP Anomaly Detection with Generative AI

## Description

This is the Final Project of the Class A Knowledge-Based Systems Engineering course on the topic of using Generative AI to detect transaction anomalies and provide an output explanation of the reasons why the transaction is an anomaly.

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
