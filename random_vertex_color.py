# -*- coding: utf-8 -*-

# Author: safina3d
# Website: safina3d.blogspot.com
# Version: 1.2
# Description: This script assigns random colors to connected vertices of a polygonal object
# in Cinema 4D using the Vertex Color Tag. It identifies connected vertex chunks and colors
# each chunk with a unique random color.


import time
import c4d
from c4d import utils, Vector, BaseObject, VariableTag
from random import uniform
from typing import List, Dict, Set

def get_random_color() -> Vector:
    """
    Returns a random color as c4d.Vector.
    
    Returns:
        c4d.Vector: A vector representing a random color.
    """
    return Vector(uniform(0.0, 1.0), uniform(0.0, 1.0), uniform(0.0, 1.0))

def build_adjacency_list(op: BaseObject) -> Dict[int, Set[int]]:
    """
    Builds an adjacency list from the polygons of the object.

    Args:
        op (BaseObject): The polygonal object in Cinema 4D.

    Returns:
        Dict[int, Set[int]]: A dictionary where each key is a vertex and the value is a set of adjacent vertices.
    """
    adjacency_list = {}
    for i in range(op.GetPolygonCount()):
        poly = op.GetPolygon(i)
        vertices = [poly.a, poly.b, poly.c, poly.d]
        for vert in vertices:
            if vert not in adjacency_list:
                adjacency_list[vert] = set()
            adjacency_list[vert].update([v for v in vertices if v != vert])
    return adjacency_list

def get_connected_chunk(adjacency_list: Dict[int, Set[int]], start_vertex: int, visited: Set[int]) -> Set[int]:
    """
    Retrieves a connected chunk of vertices starting from a start vertex.

    Args:
        adjacency_list (Dict[int, Set[int]]): The adjacency list of vertices.
        start_vertex (int): The start vertex.
        visited (Set[int]): The set of already visited vertices.

    Returns:
        Set[int]: A set of vertices forming a connected chunk.
    """
    stack = [start_vertex]
    chunk = set()

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            chunk.add(vertex)
            stack.extend(adjacency_list[vertex] - visited)

    return chunk

def get_chunks(op: BaseObject) -> List[List[int]]:
    """
    Splits the object into chunks of connected vertices.

    Args:
        op (BaseObject): The polygonal object in Cinema 4D.

    Returns:
        List[List[int]]: A list of chunks, each being a list of connected vertices.
    """
    adjacency_list = build_adjacency_list(op)
    visited = set()
    chunks = []

    for vertex in adjacency_list:
        if vertex not in visited:
            chunk = get_connected_chunk(adjacency_list, vertex, visited)
            chunks.append(list(chunk))

    return chunks

def polygons_to_vertices(op: BaseObject, polygon_list: List[int]) -> List[int]:
    """
    Converts a list of polygon indices to a list of vertex indices.

    Args:
        op (BaseObject): The polygonal object in Cinema 4D.
        polygon_list (List[int]): The list of polygon indices.

    Returns:
        List[int]: A list of vertex indices.
    """
    vertices = set()
    for polygon_index in polygon_list:
        pts = op.GetPolygon(polygon_index)
        vertices.update([pts.a, pts.b, pts.c, pts.d])
    return list(vertices)

def main() -> None:
    """
    Main function executed when the script is called.
    Colors the connected vertices of the object with random colors.
    """
    if op is None:
        return

    if op.GetType() != c4d.OBJECT_POLYGON:
        return

    vertex_color_tag = op.GetTag(c4d.Tvertexcolor)
    if vertex_color_tag is None:
        vertex_color_tag = c4d.VariableTag(c4d.Tvertexcolor, op.GetPointCount())
        op.InsertTag(vertex_color_tag)

    doc.SetActiveTag(vertex_color_tag)
    data = vertex_color_tag.GetDataAddressW()

    chunks = get_chunks(op)
    for chunk in chunks:
        color = get_random_color()
        for vertex in chunk:
            c4d.VertexColorTag.SetColor(data, None, None, vertex, color)

    c4d.EventAdd()


if __name__ == '__main__':
    main()
