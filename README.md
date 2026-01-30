# Standalone Mock Hypothesis Server

This folder contains a standalone Python script (`mock_hypothesis_server.py`) designed to simulate the external **Hypothesis Generation API**.

## Purpose
The main AI Assistant application interacts with this server to request hypothesis generation. By using this mock server, we decouple the development and testing of the AI Assistant from the real/production scientific data services.

In the future, we can simply change the API endpoint URLs in the AI Assistant's environment variables configuration to point to a **Real Hypothesis Service**, and the application will work without any code changes.

## Prerequisites
To run this server, you need:
1.  **Python 3.10+** installed on your system (WSL or Windows).
2.  **Flask** library installed.

## Setup & Running (Step-by-Step)

### Running in a Virtual Environment (Recommended)
This keeps our system clean.

1.  **Open your terminal** (PowerShell or WSL).
2.  **Navigate to this folder**:
    ```bash
    cd path/to/external_mock_services
    ```
3.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
4.  **Activate the environment**:
    *   *Windows (PowerShell)*: `.\venv\Scripts\Activate`
    *   *WSL/Linux*: `source venv/bin/activate`
5.  **Install Flask**:
    ```bash
    pip install flask
    ```
6.  **Run the Server**:
    ```bash
    python mock_hypothesis_server.py
    ```
    we should see output indicating the server is running on **port 9001**.



## Usage
Once running, this server listens on `http://0.0.0.0:9001`.
-   **Main App Configuration**: Ensure your AI Assistant's `.env` file points to this server (e.g., `http://172.17.0.1:9001` or `http://host.docker.internal:9001`).


