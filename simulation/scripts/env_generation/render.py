#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import os
import subprocess
from gazebo_msgs.srv import DeleteModel
import time
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree


def world_folder_path():
    """
    Points to the simulation/worlds
    :return:
    """
    path = __file__
    for i in range(3):
        path, _ = os.path.split(path)
    return os.path.join(path, "worlds")


def delete_model(model):
    """
    Model erasing from gazebo.
    Called every time on model recreation.
    :param model:
    :return:
    """
    delete = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
    delete(model)
    time.sleep(0.2)


def indent(elem, level=0):
    """
    This method walks through the tree and adds spaces and new lines to make it pretty.
    :param elem:
    :param level:
    :return:
    """
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def add_box(model_sdf, box):
    """
    Python wall object into xml tree
    :param model_sdf:
    :param wall:
    :return:
    """
    link = SubElement(model_sdf, 'link')
    link.set("name", box.name)

    pose = SubElement(link, 'pose')

    pose.text = string_pose(box)

    collision = SubElement(link, 'collision')
    collision.set("name", "collision")
    geometry_coll = SubElement(collision, 'geometry')
    box_coll = SubElement(geometry_coll, 'box')
    size_coll = SubElement(box_coll, 'size')
    size_coll.text = string_size(box)

    visual = SubElement(link, 'visual')
    visual.set("name", "visual")
    geometry_vis = SubElement(visual, 'geometry')
    box_vis = SubElement(geometry_vis, 'box')
    size_vis = SubElement(box_vis, 'size')
    size_vis.text = string_size(box)


def string_pose(wall):
    return str(wall.x) + " " + str(wall.y) + " " + str(wall.z) + \
           str(wall.roll) + " " + str(wall.pitch) + " " + str(wall.yaw)


def string_size(wall):
    return str(wall.box_x) + " " + str(wall.box_y) + " " + str(wall.box_z)


def spawn(model):
    launch_file = os.path.join(world_folder_path(), model.name+".sdf")
    subprocess.run('rosrun gazebo_ros spawn_model -file ' + launch_file + ' -sdf -model ' + model.name,
                   shell=True, check=True)


def add_sphere(model_sdf, sphere):
    """
    Python wall object into xml tree
    :param model_sdf:
    :param wall:
    :return:
    """
    link = SubElement(model_sdf, 'link')
    link.set("name", sphere.name)

    pose = SubElement(link, 'pose')

    pose.text = string_pose(box)

    collision = SubElement(link, 'collision')
    collision.set("name", "collision")
    geometry_coll = SubElement(collision, 'geometry')
    box_coll = SubElement(geometry_coll, 'box')
    size_coll = SubElement(box_coll, 'size')
    size_coll.text = string_size(box)

    visual = SubElement(link, 'visual')
    visual.set("name", "visual")
    geometry_vis = SubElement(visual, 'geometry')
    box_vis = SubElement(geometry_vis, 'box')
    size_vis = SubElement(box_vis, 'size')
    size_vis.text = string_size(box)


def apply(model):
    """
    Conversion of a python object into the corresponding XML tree
    :param model:
    :return:
    """
    # Delete previous model
    # delete_model(model.name)
    # Add headers
    sdf = Element('sdf')
    sdf.set("version", str(1.5))
    sdf.append(Comment('Generated on demand'))

    model_sdf = SubElement(sdf, 'model')
    model_sdf.set("name", model.name)

    stat = SubElement(model_sdf, 'static')
    stat.text = "true"
    if hasattr(model, 'steps'):
        # Body
        # walls
        for wall in model.walls:
            add_box(model_sdf, wall)

        # floor
        if model.floor is not None:
            add_box(model_sdf, model.floor)

        # steps
        for step in model.steps:
            add_box(model_sdf, step)

    if hasattr(model, 'goal'):
        add_sphere(model_sdf, model.goal.inner)
        add_sphere(model_sdf, model.goal.outter)

    # Printing into file
    indent(sdf)
    tree = ElementTree(sdf)
    with open(os.path.join(world_folder_path(), model.name + ".sdf"), "wb") as f:
        tree.write(f, encoding='utf-8', xml_declaration=True, method="xml")

    spawn(model)
