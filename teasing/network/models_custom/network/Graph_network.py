from django.db import models
from django.core.files import File
from django.conf import settings
from matplotlib import pyplot as plt
from teasingApp.models_custom.teasingApp.Graph_AL import Graph_AL
from teasingApp.models_custom.teasingApp.Graph_access_file import graph_access_file
import networkx as nx
import os
import datetime
import uuid
import matplotlib 
matplotlib.use('Agg')


class Graph(models.Model):
    image = models.ImageField(upload_to='graphs/')


class Graph_network(Graph_AL):
    def __init__(self, source: str ,site:str) -> None:
        # ilay source eto efa ilay ip no node
        super().__init__(source)
        self.modified =True
        self.list_paths ={}
        self.site_list = {}
        self.init_site(site)
        self.init_dijkstra()

    def init_dijkstra (self):
        if self.modified is not False:
            self.list_paths = {node: self.dijkstra(node) for node in self.elements}
            self.modified = False

    def init_site(self,site_source):
        all_line =graph_access_file.get_all_lines(site_source)
        for line in all_line :
            temp = line.split(':')            
            self.site_list[temp[0]] = temp[1].split(',')

    def contains_site(self ,server_ip:str , site:str):
        for a in self.site_list [server_ip]:
            if a.lower() == site.lower():
                return True
        return False   

    def get_path(self ,key ,site):
        #key na hoe ilay depart anle serveur 
        self.init_dijkstra()
        possible_paths = self.list_paths[key]
        all_keys = possible_paths.keys()
        for one in all_keys :
            if self.contains_site(one,site) is True :
                return possible_paths[one] 
        return None

    def cut_path(self , node1 ,node2 ,both_ways=True):
        print(self.adjancy_list)
        if both_ways is True:
            i=0
            for in_list in self.adjancy_list[node2]:
                if in_list[0] == node1:
                   self.adjancy_list[node2].pop(i) 
                   break
                i+=1
        i=0
        for in_list in self.adjancy_list[node1]:
            if in_list[0] == node2:
               self.adjancy_list[node1].pop(i) 
               break
            i+=1
        self.modified= True
 
        
    def prepare_image(self):
        plt.clf()
        G = nx.DiGraph()

        for node, edges in self.adjancy_list.items():
            for edge in edges:
                target_node, weight = edge
                G.add_edge(node, target_node, weight=float(weight))

        pos = nx.spring_layout(G) # type: ignore
        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=10, edge_color='gray') # type: ignore
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500) # type: ignore
        nx.draw_networkx_labels(G, pos, font_size=10) # type: ignore
        edge_labels = nx.get_edge_attributes(G, 'weight') # type: ignore
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels) # type: ignore
        
        image_path = 'network/graph.png'  # Chemin relatif par rapport au dossier `static`
        image_full_path = os.path.join(settings.STATICFILES_DIRS[0], image_path)
        plt.savefig(image_full_path, format='png')        
 
        return image_path