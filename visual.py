from __future__ import unicode_literals

import numpy as np
import pandas as pd
import json
import sys
import os
from graphviz import Digraph
import tkinter as Tkinter
import tkinter.ttk as ttk
from treelib import Node, Tree
import pdb


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
        self.initialize_user_interface()

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

        # make a tree
        result_hash = {} # hierarchy structure response
        children_hash = {}
        records_hash = {}

        for item in excel_data:
            iteritems = item['sheet_content']
            for iteritem in iteritems:
                records_hash[str(iteritem["id"])] = iteritem
                if iteritem["parent"] == None:
                    result_hash[str(iteritem["id"])] = iteritem
                else:
                    if len(children_hash) > 0 and str(iteritem["parent"]) in children_hash:
                        children_hash[str(iteritem["parent"])].append(iteritem)
                    else:
                        children_hash[str(iteritem["parent"])] = [iteritem]

        while len(children_hash.keys()) > 0:
            for key in  list(children_hash):
                parent = records_hash[key]["parent"]
                if parent is None:
                    if 'children' in result_hash[key]:
                        result_hash[key]["children"].append(children_hash[key])
                    else:
                        result_hash[key]["children"] = children_hash[key]

                else:
                    parent = str(records_hash[key]["parent"])
                    if parent in children_hash:
                        children_hash[parent].append(children_hash[key])
                    else:
                        children_hash[parent] = children_hash[key]

                del children_hash[key]

        k = list(result_hash)[0]
        print(result_hash[k])

    def initialize_user_interface(self):
        """Draw a user interface allowing the user to type
        items and insert them into the treeview
        """
        self.parent.title("Canvas Test")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="lavender")

        # Set the treeview
        self.tree = ttk.Treeview(self.parent,
                                 columns=('Dose', 'Modification date'))
        self.tree.heading('#0', text='Item')
        self.tree.heading('#1', text='Dose')
        self.tree.heading('#2', text='Modification Date')
        self.tree.column('#1', stretch=Tkinter.YES)
        self.tree.column('#2', stretch=Tkinter.YES)
        self.tree.column('#0', stretch=Tkinter.YES)
        self.tree.grid(row=4, columnspan=4, sticky='nsew')
        self.treeview = self.tree
        # Initialize the counter
        self.i = 0

    def insert_data(self):
        """
        Insertion method.
        """
        self.treeview.insert('', 'end', text="Item_"+str(self.i),
                             values=(self.dose_entry.get() + " mg",
                                     self.modified_entry.get()))
        # Increment counter
        self.i = self.i + 1

if __name__ == "__main__":
    folder_path = os.getcwd() + '/inputs' # path where the xlsx files are
    file_name = os.path.join(folder_path, 'input.xlsx')

    json_tree = JsonView()
    # json_tree.get_treeview(file_name)

    root = Tkinter.Tk()
    root.title("JSON editor")
    d = TreeView(root)
    root.mainloop()

    # tree=ttk.Treeview(root)

    # tree["columns"]=("one","two","three")
    # tree.column("#0", width=270, minwidth=270, stretch=tk.NO)
    # tree.column("one", width=150, minwidth=150, stretch=tk.NO)
    # tree.column("two", width=400, minwidth=200)
    # tree.column("three", width=80, minwidth=50, stretch=tk.NO)

    # tree.heading("#0",text="Name",anchor=tk.W)
    # tree.heading("one", text="Date modified",anchor=tk.W)
    # tree.heading("two", text="Type",anchor=tk.W)
    # tree.heading("three", text="Size",anchor=tk.W)

    # # Level 1
    # folder1=tree.insert("", 1, 1, text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
    # folder2=tree.insert(folder1, 1, 5, text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
    # folder2=tree.insert(folder1, 1, 4, text="Folder 1", values=("23-Jun-17 11:05","File folder",""))
    # # tree.insert("", 2, "", text="text_file.txt", values=("23-Jun-17 11:25","TXT file","1 KB"))
    # # Level 2
    # tree.insert(folder2, "end", 2, text="photo1.png", values=("23-Jun-17 11:28","PNG file","2.6 KB"))
    # tree.insert(folder2, "end", 3, text="photo2.png", values=("23-Jun-17 11:29","PNG file","3.2 KB"))
    # tree.insert(folder2, "end", 4, text="photo3.png", values=("23-Jun-17 11:30","PNG file","3.1 KB"))

    # tree.pack(side=tk.TOP,fill=tk.X)
    # root.mainloop()

