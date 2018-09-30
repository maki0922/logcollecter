#!/usr/bin/env python
# coding: UTF-8

import os
import sys
import lib.utils
import lib.provision as provision
import lib.provision as collect

class LogCollect:

    def __init__(self, _node, _dict_tool_conf):
        self.node = _node
        self.dict_tool_conf = _dict_tool_conf

    def prepare(self):
      return 0
