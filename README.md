# wm2many
This repository contains a code converter application built using Streamlit. The application allows you to convert Wardley Mapping WM files into manu formats. TOML, JSON, GRAPH and CYPHER.

[![Twitter Follow](https://img.shields.io/twitter/follow/mcraddock?style=social)](https://twitter.com/mcraddock)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wm2json.streamlit.app/)

# Installation
To run the code converter, please follow these steps:

Clone the repository to your local machine:

bash
Copy code
git clone https://github.com/your-username/code-converter.git

Choose the desired conversion option from the sidebar:

- JSON to TOML: Converts a JSON file to TOML format.
- WM to TOML: Converts a Wardley Map in WM format to TOML.
- WM to JSON: Converts a Wardley Map in WM format to JSON.
- WM to GRAPH: Converts a Wardley Mapin WM format to JSON GRAPH.
- WM to CYPHER: Converts a Wardley Map in WM format to CYPHER.
- WM to GML: Converts a Wardley Map in WM format to GML.
- Follow the instructions and upload the required files or enter the necessary information to perform the conversion.

Once the conversion is complete, you can view the converted content and download the resulting file in the specified format.

## Notes

- The application utilizes the `streamlit_option_menu` library for creating dropdown menus with icons.
- The `parse_wardley_map` function is used to parse the Wardley Map text and extract relevant information.
- The `swap_xy` function swaps the x and y coordinates in a given format.
- The application uses the Streamlit library to create the user interface and handle file uploads and downloads.
- Conversion between JSON and TOML formats is performed using the `json` and `toml` libraries, respectively.
- The application makes use of the `requests` library to fetch Wardley Maps from the onlinewardleymaps.com API.

Feel free to explore the code and adapt it to your needs. Happy coding!
Please let me know if there's anything else I can assist you with!
