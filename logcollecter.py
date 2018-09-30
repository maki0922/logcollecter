#!/usr/bin/env python
# coding: UTF-8
import os
import sys
import lib.utils
import lib.provision
import lib.collect
from pprint import pprint

TOOL_CONFIG='collect.ini'

def _main():

    # load & setting from command & config 
    prov = lib.provision.ProvisionLogCollect()    
    opts, dict_tool_ini, dict_tool_conf, dict_nodes = prov.load_data(TOOL_CONFIG) 

    prov.inspect_opts(opts,dict_tool_ini)
    li_target_nodes = prov.inspect_nodes(opts,dict_nodes)

    # Loop Target Node & Get log
    for _node in li_target_nodes:

        #try:
        #    dict_log = prov.get_log_list(_node)
        #except:
            
        c = lib.collect.LogCollect(_node, dict_tool_conf)

        print _node

    #print opts
    #pprint (dict_tool_conf.items())
    #pprint (dict_nodes.items())

    sys.stdout.write('success!!\n')
    sys.exit()

if __name__ == "__main__":
    _main()

# Powerd by : https://www.sejuku.net/blog/23647
