import streamlit as st

def dfs(graph, element, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for link in graph[element]:
        if link['src'] == start and link['tgt'] not in visited:
            dfs(graph, link['tgt'], visited)

    return visited
