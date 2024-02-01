import streamlit as st
from streamlit_option_menu import option_menu
import requests, re, json, toml
from ast import Index
from networkx.readwrite import json_graph
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components


def swap_xy(xy):
  new_xy = re.findall("\[(.*?)\]", xy)
  if new_xy:
    match = new_xy[0]
    match = match.split(sep = ",")
    match = match[::-1]
    new_xy = ('[' + match[0].strip() + ',' + match[1] + ']')
    return (new_xy)
  else:
    new_xy=""
    return (new_xy)

def parse_wardley_map(map_text):
    lines = map_text.strip().split("\n")
    title, evolution, anchors, components, nodes, links, evolve, pipelines, pioneers, market, blueline, notes, annotations, comments, style = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    current_section = None

    for line in lines:
        if line.startswith("//"):
            comments.append(line)

        elif line.startswith("evolution"):
            evolution.append(line)

        elif "+<>" in line:
            blueline.append(line)

        elif line.startswith("title"):
            name = ' '.join(line.split()[1:])
            title.append(name)

        elif line.startswith("anchor"):
            name = line[line.find(' ') + 1:line.find('[')].strip()
            anchors.append(name)

        elif line.startswith("component"):
            stage = ""
            pos_index = line.find("[")
            if pos_index != -1:
                new_c_xy = swap_xy(line)
                number = json.loads(new_c_xy)
                if 0 <= number[0] <= 0.17:
                    stage = "genesis"
                elif 0.18 <= number[0] <= 0.39:
                    stage = "custom"
                elif 0.31 <= number[0] <= 0.69:
                    stage = "product"
                elif 0.70 <= number[0] <= 1.0:
                    stage = "commodity"
                else:
                    visibility = ""
                if 0 <= number[1] <= 0.20:
                    visibility = "low"
                elif 0.21 <= number[1] <= 0.70:
                    visibility = "medium"
                elif 0.71 <= number[1] <= 1.0:
                    visibility = "high"
                else:
                    visibility = ""               
            else:
                new_c_xy = ""

            name = line[line.find(' ') + 1:line.find('[')].strip()

            label_index = line.find("label")
            if label_index != -1:
                label = line[label_index+len("label")+1:]
                label = swap_xy(label)
            else:
                label = ""

            components.append({"name": name, "desc": "", "evolution": stage, "visibility": visibility, "pos": new_c_xy, "labelpos": label})

        elif line.startswith("pipeline"):
            new_c_xy = swap_xy(line)
            name = line[line.find(' ') + 1:line.find('[')].strip()
            pipelines.append({"name": name, "desc": "", "pos": new_c_xy, "labelpos": ""})

        elif line.startswith("links"):
            links.append(line)

        elif line.startswith("evolve"):
            new_c_xy = swap_xy(line)
            name = re.findall(r'\b\w+\b\s(.+?)\s\d', line)[0]
            label_index = line.find("label")
            if label_index != -1:
                label = line[label_index+len("label")+1:]
            else:
                label = ""
            label = swap_xy(label)
            evolve.append({"name": name, "desc": "", "pos": new_c_xy, "labelpos": label})

        elif line.startswith("pioneer"):          
            pioneers.append(line)

        elif line.startswith("note"):
            name = line[line.find(' ') + 1:line.find('[')].strip()
            pos_index = line.find("[")
            if pos_index != -1:
                new_c_xy = swap_xy(line)
            else:
                new_c_xy = ""
            notes.append({"name": name, "desc": "", "pos": new_c_xy, "labelpos": ""})   
                  
        elif line.startswith("annotations"):
            new_c_xy = swap_xy(line)
            annotations.append({"name": line, "desc": "", "pos": new_c_xy})
            continue

        elif line.startswith("annotation"):
            new_c_xy = swap_xy(line)
            number = re.findall(r'\d+', line)
            name = line[line.index(']')+1:].lstrip()
            annotations.append({"number": number[0], "name": name, "desc": "", "pos": new_c_xy})

        elif line.startswith("market"):
            name = line[line.find(' ') + 1:line.find('[')].strip()
            new_c_xy = swap_xy(line)
            label_index = line.find("label")
            if label_index != -1:
                label = line[label_index+len("label")+1:]
            else:
                label = ""
            label = swap_xy(label)
            market.append({"name": name, "desc": "", "pos": new_c_xy, "labelpos": label})

        elif line.startswith("style"):
            style.append(line)

        elif "->" in line:
            source, target = line.strip().split("->")
            source = source.strip()
            target = target.strip()
            links.append({"src": source, "tgt": target})
        else:
            continue

    return {
        "title" : title,
        "anchors" : anchors,
        "evolution" : evolution,
        "components": components,
        "links": links,
        "evolve": evolve,
        "markets": market,
        "pipelines": pipelines,
        "pioneers": pioneers,
        "notes": notes,
        "blueline": blueline,
        "style": style,
        "annotations": annotations,
        "comments": comments,
    }

st.set_page_config(
    page_title="JSON to TOML file converter",
    layout="wide"
)

with st.sidebar:
    selected = option_menu(
        "Choose conversion",
        ["WM to JSON", "WM to TOML", "WM to GRAPH", "WM to CYPHER", "JSON to TOML"],
        icons=["gear"],
        menu_icon="robot",
        default_index=0,
    )

if selected == "JSON to TOML":
    st.title("JSON to TOML file converter")
    st.write(
        """  

            """
    )

    st.write(
        """  
    Let's convert your Wardley Map in JSON to TOML

            """
    )

    st.write(
        """  

            """
    )
    json_file = st.file_uploader("UPLOAD JSON FILE")
    st.info(
        f"""
                👆 Upload your json file.
                
                """
    )


    if json_file is not None:
        json_text = json_file.read()

        st.write("JSON CONTENT")
        st.code(json.loads(json_text))

        toml_content = toml.dumps(json.loads(json_text))
        st.write("TOML FILE CONTENT")
        st.code(toml_content, language="toml")
        toml_file_name = json_file.name.replace(".json", ".toml")
        st.download_button(
            "DOWNLOAD TOML FILE", data=toml_content, file_name=toml_file_name
        )
        
elif selected == "WM to TOML":
    st.title("WM to TOML Converter")
    st.write(
        """  
            """
    )
    st.write(
        """  
    Let's convert your Wardley Map in WM to TOML
            """
    )
    
    st.write(
        """  
            """
    )
    
    # Map ID from onlinewardleymapping
    map_id=''
    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")
    
    # Fetch map using onlinewardleymapping api
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    response = requests.get(url)
    
    # Check if the map was found
    if response.status_code == 200:
        map_data = response.json()
        wardley_map_text = map_data['text']

# Parse the Wardley map text
        parsed_map = parse_wardley_map(wardley_map_text)
        wardley_map_toml = toml.dumps(parsed_map)
        st.write("TOML FILE CONTENT")
        st.code(wardley_map_toml, language="toml")  
        
        toml_file_name = map_id + '.toml'
        st.download_button(
            "DOWNLOAD TOML FILE",
            data=wardley_map_toml,
            file_name=toml_file_name
        )  

elif selected == "WM to JSON":
    st.title("WM to JSON File Converter")
    st.write(
        """  
            """
    )
    st.write(
        """  
    Let's convert your Wardley Map in WM to JSON
            """
    )
    
    st.write(
        """  
            """
    )
    
    # Map ID from onlinewardleymapping
    map_id=''
    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")
    
    # Fetch map using onlinewardleymapping api
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    response = requests.get(url)
    
    # Check if the map was found
    if response.status_code == 200:
        map_data = response.json()
        wardley_map_text = map_data['text']
        
        # Parse the Wardley map text
        parsed_map = parse_wardley_map(wardley_map_text)
        
        # Convert the parsed map to JSON
        wardley_map_json = json.dumps(parsed_map, indent=2)
        st.write("JSON FILE CONTENT")
        st.code(wardley_map_json, language="json")
        
        json_file_name = map_id + '.json'
        st.download_button(
            "DOWNLOAD JSON FILE",
            data=wardley_map_json,
            file_name=json_file_name
        )

elif selected == "WM to GRAPH":
    st.title("WM to GRAPH Converter")
    st.write(
        """
    Let's convert your Wardley Map in WM to GRAPH and visualize it.
            """
    )

    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")

    # Fetch map using onlinewardleymapping API
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    response = requests.get(url)

    if response.status_code == 200:
        map_data = response.json()
        wardley_map_text = map_data['text']

        # Convert the Wardley map text to JSON (using your existing conversion logic)
        parsed_map = parse_wardley_map(wardley_map_text)

        # Initialize the graph
        G = nx.DiGraph()

        # Add nodes with stage (evolution) and visibility
        for component in parsed_map["components"]:
            G.add_node(component["name"], stage=component["evolution"], visibility=component["visibility"])

        # Add edges
        for link in parsed_map["links"]:
            G.add_edge(link["src"], link["tgt"])

        # Initialize a PyVis network and add nodes and edges from the NetworkX graph
        net = Network(height="950px", width="100%", bgcolor="#222222", font_color="white")
        for node, node_attrs in G.nodes(data=True):
            net.add_node(node, label=node, title=str(node_attrs), color="#f68b24" if node_attrs.get('type', '') == 'component' else "#16a085")
        for source, target in G.edges():
            net.add_edge(source, target)

        output_path = "graph.html"
        net.save_graph(output_path)
        
        # Read the content of the saved HTML file
        with open(output_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        
        # Display the HTML content in Streamlit
        components.html(html_content, height=800)

        # Convert the graph to a JSON format for download
        graph_json = json_graph.node_link_data(G)  # Convert the graph to a JSON-compatible dict
        graph_json_str = json.dumps(graph_json, indent=2)  # Convert the dict to a pretty-printed JSON string

        # Add a download button for the JSON file
        st.download_button(label="Download Graph JSON",
                           data=graph_json_str,
                           file_name="graph.json",
                           mime="application/json")


elif selected == "WM to CYPHER":
    st.title("WM to CYPHER Converter")
    st.write(
        """
    Let's convert your Wardley Map in WM to Cypher queries for Neo4j
            """
    )

    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")

    # Fetch map using onlinewardleymapping API
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    response = requests.get(url)

    if response.status_code == 200:
        map_data = response.json()
        wardley_map_text = map_data['text']

        # Convert the Wardley map text to JSON (using your existing conversion logic)
        parsed_map = parse_wardley_map(wardley_map_text)

        # Initialize Cypher query list
        cypher_queries = []

        # Generate Cypher queries for nodes
        for component in parsed_map["components"]:
            query = f"CREATE (:{component['name']} {{stage: '{component['evolution']}', visibility: '{component['visibility']}'}})"
            cypher_queries.append(query)

        # Generate Cypher queries for relationships
        for link in parsed_map["links"]:
            query = f"MATCH (a), (b) WHERE a.name = '{link['src']}' AND b.name = '{link['tgt']}' CREATE (a)-[:RELATES_TO]->(b)"
            cypher_queries.append(query)

        # Combine all queries into a single script
        cypher_script = "\n".join(cypher_queries)

        # Display Cypher script
        st.write("CYPHER FILE CONTENT")
        st.code(cypher_script, language="cypher")

        # Add a download button for the Cypher script
        st.download_button(label="Download Cypher Script",
                           data=cypher_script,
                           file_name="wardley_map_to_cypher.cql",
                           mime="text/plain")
