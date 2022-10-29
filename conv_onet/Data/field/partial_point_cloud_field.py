#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np

from conv_onet.Data.field.field import Field


class PartialPointCloudField(Field):
    ''' Partial Point cloud field.

    It provides the field used for partial point cloud data. These are the points
    randomly sampled on the mesh and a bounding box with random size is applied.

    Args:
        file_name (str): file name
        transform (list): list of transformations applied to data points
        part_ratio (float): max ratio for the remaining part
    '''

    def __init__(self, file_name, transform=None, part_ratio=0.7):
        self.file_name = file_name
        self.transform = transform
        self.part_ratio = part_ratio

    def load(self, model_path, idx, category):
        ''' Loads the data point.

        Args:
            model_path (str): path to model
            idx (int): ID of data point
            category (int): index of category
        '''
        file_path = os.path.join(model_path, self.file_name)

        pointcloud_dict = np.load(file_path)

        points = pointcloud_dict['points'].astype(np.float32)
        normals = pointcloud_dict['normals'].astype(np.float32)

        side = np.random.randint(3)
        xb = [points[:, side].min(), points[:, side].max()]
        length = np.random.uniform(self.part_ratio * (xb[1] - xb[0]),
                                   (xb[1] - xb[0]))
        ind = (points[:, side] - xb[0]) <= length
        data = {
            None: points[ind],
            'normals': normals[ind],
        }

        if self.transform is not None:
            data = self.transform(data)

        return data

    def check_complete(self, files):
        ''' Check if field is complete.

        Args:
            files: files
        '''
        complete = (self.file_name in files)
        return complete
