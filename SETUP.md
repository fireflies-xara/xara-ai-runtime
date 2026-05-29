\# XARA AI Setup Guide



\## Prerequisites



\* Python 3.10

\* Intel RealSense SDK

\* Intel RealSense D435 Camera

\* Git



\---



\## Clone Repository



git clone <repository-url>



cd xara-AI



\---



\## Create Virtual Environment



python -m venv venv



\---



\## Activate Virtual Environment



Windows:



.\\venv\\Scripts\\activate



\---



\## Install Dependencies



pip install -r requirements.txt



\---



\## Verify RealSense Camera



python app/camera/camera\_stream.py



Expected:



\* RGB Stream Opens

\* ESC closes stream



\---



\## Project Structure



camera\_stream.py



Responsible for:

D435 → RGB Frames



person\_detector.py



Responsible for:

RGB Frame → Person Detection



json\_generator.py



Responsible for:

Detection → JSON



api\_client.py



Responsible for:

JSON → Backend API



main.py



Responsible for:

Pipeline Orchestration



Camera

↓

Detection

↓

JSON

↓

Backend



\---



\## Troubleshooting



If pyrealsense2 missing:



python -m pip install pyrealsense2



If camera busy:



Close Intel RealSense Viewer



If venv inactive:



.\\venv\\Scripts\\activate



