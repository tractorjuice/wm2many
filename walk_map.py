import streamlit as st

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for link in graph['links']:
        if link['src'] == start and link['tgt'] not in visited:
            dfs(graph, link['tgt'], visited)

    return visited
