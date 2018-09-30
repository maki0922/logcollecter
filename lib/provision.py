#!/usr/bin/env python
# coding: UTF-8

import os
import sys
import copy
import lib.utils
import utils

class ProvisionLogCollect:

    def __init__(self):
        pass

    def load_data(self, inifile):

        # get options
        obj_opt = lib.utils.OptionManager()
        args = obj_opt.get()

        # get inifile
        obj_config = lib.utils.ConfigManager()
        dict_ini = obj_config.get_inifile(inifile)

        # get tool&node setting
        dict_tool = obj_config.get_ymlfile(dict_ini['GENERAL']['log_config_path'])
        dict_node = obj_config.get_ymlfile(dict_ini['GENERAL']['node_config_path'])

        return args, dict_ini, dict_tool, dict_node

    def inspect_opts(self, _opts, ini_params):

        # if not selected node, raise 
        if _opts.grp == None and \
            _opts.node_list == None and \
            _opts.list_file == None:

            sys.stderr.write('selected parameter is insufficient')
            raise ValueError

        # if not selected log optoin,
        # perform setting to acquire LOG for two generations.
        if _opts.file_generation == None and \
            _opts.time_range == None:

            try:
                _opts.file_generation = ini_params['GENERAL']['file_generation']
            except KeyError:
                sys.stderr.write('Invalid setting at inifile .\n' )
                raise

    def inspect_nodes(self, _opts, _dict_nodes):

        _node_list = []

        if _opts.node_list:
            _node_list = copy.deepcopy(_opts.node_list)
      
        if _opts.grp:
            for _node in _dict_nodes['nodes']:
                try:
                   _spam = set(_opts.grp)
                   _ham = set(_dict_nodes['nodes'][_node]['group'])

                   if _spam.intersection(_ham):
                       _node_list.append(_node)
                except:
                   pass

        if _opts.list_file:

            for _node in _opts.list_file:
                _node_list.append(_node.rstrip('\r\n'))
            _opts.list_file.close

        li_nodes_uniq = utils.del_duplicate_list(_node_list)

        for _node in li_nodes_uniq:
            try:
                _log_result = _dict_nodes['nodes'][_node]['log']
            except :
                sys.stderr.write(' \"%s\" Invalid setting in node defination file.\n' % _node)
                raise

        return li_nodes_uniq

# Powerd by https://blog1.erp2py.com/2012/02/pythonset.html
