# -*- coding: utf-8 -*-

# Author: safina3d
# Website: safina3d.blogspot.com
# Version: 1.1
# Description: Assign random color to connected vertices using  Vertex Color Tag

import c4d
from c4d import utils, Vector, BaseContainer
from random import randint


def get_random_color():
    """ Return a random color as c4d.Vector """

    def get_random_value():
        """ Return a random value between 0.0 and 1.0 """
        return randint(0, 255) / 256.0

    return Vector(get_random_value(), get_random_value(), get_random_value())


def get_connected_polygons(obj, remaining_polygons):
    # type: (PolygonObject, List[int]) -> List[int]
    bs = obj.GetPolygonS()
    bs.DeselectAll()
    bs.Select(remaining_polygons[0])
    utils.SendModelingCommand(command=c4d.MCOMMAND_SELECTCONNECTED,
                              list=[obj],
                              mode=c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
                              bc=BaseContainer(),
                              doc=doc)
    result = []
    for polygon_index in remaining_polygons:
        if bs.IsSelected(polygon_index):
            result.append(polygon_index)

    return result


def polygons_to_vertices(op, polygon_list):
    # type: (BaseObject, List[int]) -> List[int]
    vertices = []
    for polygon_index in polygon_list:
        pts = op.GetPolygon(polygon_index)
        vertices += [pts.a, pts.b, pts.c, pts.d]

    return list(set(vertices))


def get_chunks(op, remaining_polygons):
    # type: (BaseObject, List[int]) -> List[List[int]]
    result = []
    while len(remaining_polygons) > 0:
        connected_polygons = get_connected_polygons(op, remaining_polygons)
        result.append(polygons_to_vertices(op, connected_polygons))
        remaining_polygons = list(set(remaining_polygons).difference(connected_polygons))

    return result


def main():
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

    remaining_polygons = list(range(op.GetPolygonCount()))

    chunks = get_chunks(op, remaining_polygons)
    for chunk in chunks:
        color = get_random_color()
        for vertex in chunk:
            c4d.VertexColorTag.SetColor(data, None, None, vertex, color)

    c4d.EventAdd()


if __name__ == '__main__':
    main()
