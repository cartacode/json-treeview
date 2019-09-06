from __future__ import unicode_literals

import numpy as np
import pandas as pd
import json
import sys
import os
import copy
from graphviz import Digraph
import tkinter as Tkinter
import tkinter.ttk as ttk
from treelib import Node, Tree
import pdb


class Node:
    def __init__(self, name, obj=None):
        self.name = name
        self.obj = obj

class TreeView(Tkinter.Frame):
    '''
    classdocs
    '''
    def __init__(self, parent):
        '''
        Constructor
        '''
        Tkinter.Frame.__init__(self, parent)
        self.parent=parent
        self.item_counts = 0
        self.headers = []
        self.idx = 1 # index number of node
        self.node_hash = {}

    """
        creates a json view from excel file
    """
    def get_data_from_excel(self, filename):
        # read data from excel
        xl_file = pd.read_excel(file_name, sheet_name=None)
        excel_data = []
        for sheet_name in xl_file:
            sheet_detail = { 'sheet_name': sheet_name }
            sheet_content = []

            row_counts = xl_file[sheet_name].index.stop
            self.headers = list(xl_file[sheet_name])

            for idx in range(0, row_counts):
                row_data = {}
                for row_name in xl_file[sheet_name][:1]:
                    if row_name == "parent":
                        try:
                            row_data[row_name] = str(int(xl_file[sheet_name][row_name][idx]))
                        except:
                            row_data[row_name] = None
                    else:
                        row_data[row_name] = str(xl_file[sheet_name][row_name][idx])
                sheet_content.append(row_data)
            sheet_detail['sheet_content'] = sheet_content
            excel_data.append(sheet_detail)

        return excel_data

    # Create your views here.
    def get_treeview(self, filename):
        excel_data = self.get_data_from_excel(filename)
        self.initialize_user_interface()

        for item in excel_data:
            iteritems = item['sheet_content']
            items_tree = self.treeify(iteritems)
        
        self.insert_data("", 0, 0, "treeview", ())
        for item in self.node_hash.values():
            set_value_obj = ()
            for key_of_obj in item['info']:
                set_value_obj = set_value_obj + (item['info'][key_of_obj],)
            print("@@@@@@@@@@@@@@@@@@@@: ", item['parent'], item['idx'], "****", item)
            self.insert_data(item['parent'], item['node_type'], item['idx'], item['text'], set_value_obj)

    def treeify(self, elements, idAttr='id', parentAttr='parent', childrenAttr='children'):
        treeList = []
        lookup = {}

        for element in elements:
            
            lookup[element[idAttr]] = element
            element[childrenAttr] = []

        for element in elements:
            parent_idx = 0
            node_type = "end"
            if element[parentAttr] in self.node_hash:
                if 'idx' in self.node_hash[element[parentAttr]]:
                    parent_idx = self.node_hash[element[parentAttr]]['idx']
                    node_type = self.idx

            info = copy.deepcopy(element)
            del info['children']
            self.node_hash[element[idAttr]] = {
                'idx': self.idx,
                'parent': parent_idx,
                'node_type': node_type,
                'text': element['keyword singular de'],
                'info': info
            }

            self.idx = self.idx + 1

            if element[parentAttr] is not None:
                lookup[element[parentAttr]][childrenAttr].append(element)
            else:
                treeList.append(element)

        return treeList

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("Canvas Test")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="lavender")

        # Set the treeview
        self.tree = ttk.Treeview(self.parent)
        print('initialize view: ', self.headers)

        self.tree["columns"]=(self.headers)
        for i, header in enumerate(self.headers):
            self.tree.column('#{}'.format(str(i)), stretch=Tkinter.YES)

        for i, header in enumerate(self.headers, start=1):
            print('#{}'.format(str(i)), header)
            self.tree.heading('#{}'.format(str(i)), text=header)

        self.tree.grid(row=len(self.headers)+1, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.item_counts = 0

    def insert_data(self, target="", node_type="end", idx=1, text="item", set_value_obj=None):
        """
        Insertion method.
        """
        self.treeview.insert(target, node_type, idx, text=text,
                             values=set_value_obj)
        # Increment counter
        self.item_counts = self.item_counts + 1

if __name__ == "__main__":
    folder_path = os.getcwd() + '/inputs' # path where the xlsx files are
    file_name = os.path.join(folder_path, 'input.xlsx')

    root = Tkinter.Tk()
    root.title("JSON TreeView")
    tree = TreeView(root)
    tree.get_treeview(file_name)
    root.mainloop()

