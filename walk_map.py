import streamlit as st

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)
    
    #st.write(start)  # or do whatever you want to do with this node

    for link in graph['links']:
        if link['src'] == start and link['tgt'] not in visited:
            dfs(graph, link['tgt'], visited)

    return visited
