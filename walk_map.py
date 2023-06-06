import streamlit as st

def dfs(map, start, visited=None):
    if visited is None:
        visited = set()

    visited.add(start)

    for link in map['links']:
        if link['src'] == start and link['tgt'] not in visited:
            dfs(map, link['tgt'], visited)

    return visited
