#!/usr/bin/python
# -*- coding: utf-8 -*-
global_dict = None


def init():
    global global_dict
    global_dict = {}


def set_value(name, value):
    global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return global_dict[name]
    except KeyError:
        return defValue
