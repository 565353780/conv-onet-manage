#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import open3d as o3d

from conv_onet.Module.detector import Detector


def demo():

    #  mesh_file_path = \
        #  "/home/chli/chLi/ScanNet/objects/scene0000_00/37_bed.ply"
    #  mesh = o3d.io.read_triangle_mesh(mesh_file_path)
    #  points = np.array(mesh.vertices)

    mesh_file_path = \
        "/home/chli/chLi/ShapeNet/Core/ShapeNetCore.v2/" + \
        "02691156/" + \
        "222c0d99446148babe4274edc10c1c8e/" + \
        "models/model_normalized.obj"
    mesh = o3d.io.read_triangle_mesh(mesh_file_path)
    pcd = mesh.sample_points_uniformly(2000000)
    points = np.array(pcd.points)
    box = pcd.get_axis_aligned_bounding_box()
    print(box)
    print(box.get_extent())

    point_idx_array = np.arange(0, points.shape[0])
    sample_point_idx_array = np.random.choice(point_idx_array,
                                              int(points.shape[0] / 2),
                                              replace=False)
    sample_points = points[sample_point_idx_array]

    detector = Detector()
    detector.detectPointArray(sample_points)
    return True
