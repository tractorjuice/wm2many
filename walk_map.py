import streamlit as st

def dfs(map, element, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for link in map[element]:
        if element['src'] == start and element['tgt'] not in visited:
            dfs(map, link['tgt'], visited)

    return visited
