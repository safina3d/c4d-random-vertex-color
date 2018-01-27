# -*- coding: utf-8 -*-

# Author: safina3d
# Website: safina3d.blogspot.com
# Description: Assign random color to connected vertices using  Vertex Color Tag

import c4d
from c4d import utils, Vector
from random import randint


def get_random_color():
    """ Return a random color as c4d.Vector """

    def get_random_value():
        """ Return a random value between 0.0 and 1.0 """
        return randint(0, 255) / 256.0

    return Vector(get_random_value(), get_random_value(), get_random_value())


def get_connected_polygons(nbr, start_index):
    # type: (Neigbour, int) -> int[]
    result = [start_index]
    to_do = []
    done = []
    current = start_index

    while current is not None:
        connected_polygons = filter(lambda v: v != -1 and v not in result, nbr.GetPolyInfo(current)["face"])
        result += connected_polygons
        done.append(current)
        to_do += filter(lambda v: v not in done, connected_polygons)
        current = to_do.pop() if len(to_do) else None

    return result


def polygons_to_vertices(op, polygon_list):
    # type: (BaseObject, int[]) -> int[]
    vertices = []
    for polygon_index in polygon_list:
        pts = op.GetPolygon(polygon_index)
        vertices += [pts.a, pts.b, pts.c, pts.d]
    return list(set(vertices))


def get_chunks(nbr, op, remaining_polys):
    # type: (Neigbour, BaseObject, int[]) -> int[][]
    _chunks = []

    while len(remaining_polys) > 0:
        connected_polygons = get_connected_polygons(nbr, remaining_polys[0])
        _chunks.append(polygons_to_vertices(op, connected_polygons))
        remaining_polys = list(set(remaining_polys).difference(connected_polygons))

    return _chunks


def main():
    if op is None:
        return

    if c4d.OBJECT_POLYGON != op.GetType():
        return

    neigbour = utils.Neighbor()
    neigbour.Init(op)

    vertex_color_tag = op.GetTag(c4d.Tvertexcolor)

    if vertex_color_tag is None:
        vertex_color_tag = c4d.VariableTag(c4d.Tvertexcolor, op.GetPointCount())
        op.InsertTag(vertex_color_tag)

    doc.SetActiveTag(vertex_color_tag)
    data = vertex_color_tag.GetDataAddressW()

    remaining_polys = range(op.GetPolygonCount())

    chunks = get_chunks(neigbour, op, remaining_polys)

    for chunk in chunks:
        color = get_random_color()
        for vertex in chunk:
            c4d.VertexColorTag.SetColor(data, None, None, vertex, color)

    c4d.EventAdd()


if __name__ == '__main__':
    main()
