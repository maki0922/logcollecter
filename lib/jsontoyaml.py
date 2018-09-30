#!/usr/bin/env python
# coding: UTF-8

import os
import sys
import json
import ConfigParser
import yaml
import ast
import re
import api
import collections 

class JsonToYaml(object):

    def __init__(self, base_path, envfile):

        ##self.config = ConfigParser.SafeConfigParser()
        self.base_path = base_path
        self.envfile = envfile

        # load environment
        f = open(self.envfile, "r")
        #self.dict_json = json.load(f,object_pairs_hook=collections.OrderedDict)
        self.dict_json = json.load(f)

        self.dc = self.dict_json["default_attributes"]["default"]["common"]["dc"]
        self.inventory_buf = ""
        self.inventory_buf_grp = "\n[compute:children]\n"
        self.inventory_buf_cp = ""

        # make dir & set output path
        self.dir_path_list = {}
        self.make_dir()

    def start_process(self):
        self.create_host_vars()
        self.create_group_vars()
        self.create_inventory()

    def make_dir(self):
        # set dir path of group_vars
        self.dir_path_list['group_vars'] = os.path.normpath(os.path.join(self.base_path, "../ansible/group_vars/production_%s/" % self.dc))
        # set dir path of inventory
        self.dir_path_list['inventory'] = os.path.normpath(os.path.join(self.base_path,  "../ansible/inventory/"))
        # set dir path of host_vars
        self.dir_path_list['host_vars'] = os.path.normpath(os.path.join(self.base_path, "../ansible/host_vars/"))
        ## set dir path of group_vars/production_xx/endpoint
        self.dir_path_list['group_vars_endpoint'] = os.path.normpath(os.path.join(self.dir_path_list['group_vars'], "endpoint"))

        # create dirs
        api.make_dir(self.dir_path_list)

    def create_host_vars(self):

        dict_corosync_cp = self.dict_json["default_attributes"]["default"]["pacemaker"]["compute"]

        for count in range(len(dict_corosync_cp)):
            self.inventory_buf_cp = self.inventory_buf_cp + "\n[cluster_%s]\n" % dict_corosync_cp[count]["node_list"][0]
            self.inventory_buf_grp = self.inventory_buf_grp + "cluster_%s\n" % dict_corosync_cp[count]["node_list"][0]

            for cp_node in dict_corosync_cp[count]["node_list"]:
                self.inventory_buf_cp = self.inventory_buf_cp + "%s\n" % cp_node
                dict_cp = self.dict_json["default_attributes"][cp_node]
                api.writer(os.path.join(self.dir_path_list['host_vars'],"%s.yml" % cp_node),yaml.safe_dump(dict_cp,default_flow_style=False),"w")

    def create_group_vars(self):
        dict_common = {}
        list_common = ["common","contrail", "keystone", "nova", "neutron"]

        for component in list_common:
            dict_tmp = {component: self.dict_json["default_attributes"]["default"][component]}
            dict_common.update(dict_tmp)

        dict_keystone_user = {"keystone_user": self.dict_json["default_attributes"]["default"]["keystone_user"]}
        dict_endpoint = {"endpoint": self.dict_json["default_attributes"]["default"]["endpoint"]}

        api.writer(os.path.join(self.dir_path_list['group_vars'],"common.yml"),yaml.safe_dump(dict_common,default_flow_style=False),"w")
        api.writer(os.path.join(self.dir_path_list['group_vars'],"keystone_user.yml"),yaml.safe_dump(dict_keystone_user,default_flow_style=False),"w")
        api.writer(os.path.join(self.dir_path_list['group_vars_endpoint'],"%s_endpoint.yml" % self.dc),yaml.safe_dump(dict_endpoint,default_flow_style=False),"w")

    def create_inventory(self):
        
        # output inventory file
        self.inventory_buf = self.inventory_buf + self.inventory_buf_cp
        self.inventory_buf = self.inventory_buf + self.inventory_buf_grp
        self.inventory_buf = self.inventory_buf + "\n[production_%s:children]\ncompute\n" % self.dc
        api.writer(os.path.join(self.dir_path_list['inventory'], "production_%s" % self.dc),self.inventory_buf, 'w')
