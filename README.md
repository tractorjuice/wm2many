# owm2json
This repository contains a code converter application built using Streamlit. The application allows you to convert JSON files to TOML format and also convert Wardley Maps in different formats to either JSON or TOML.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wm2json.streamlit.app/)

#Installation
To run the code converter, please follow these steps:

Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-username/code-converter.git
Navigate to the project directory:

bash
Copy code
cd code-converter
Install the required dependencies:

Copy code
pip install -r requirements.txt
Usage
Run the Streamlit application:

arduino
Copy code
streamlit run app.py
Access the application through your web browser using the provided URL (typically http://localhost:8501).

Choose the desired conversion option from the sidebar:

JSON to TOML: Converts a JSON file to TOML format.
WM to TOML: Converts a Wardley Map in WM format to TOML.
WM to JSON: Converts a Wardley Map in WM format to JSON.
Follow the instructions and upload the required files or enter the necessary information to perform the conversion.

Once the conversion is complete, you can view the converted content and download the resulting file in the specified format.

Notes
The application utilizes the streamlit_option_menu library for creating dropdown menus with icons.
The parse_wardley_map function is used to parse the Wardley Map text and extract relevant information.
The swap_xy function swaps the x and y coordinates in a given format.
The application uses the Streamlit library to create the user interface and handle file uploads and downloads.
Conversion between JSON and TOML formats is performed using the json and toml libraries, respectively.
The application makes use of the requests library to fetch Wardley Maps from the onlinewardleymaps.com API.
Feel free to explore the code and adapt it to your needs. Happy coding!
