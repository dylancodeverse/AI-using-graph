from teasingApp.models_custom.teasingApp.Graph_AL import Graph_AL
from teasingApp.models_custom.teasingApp.Graph_access_file import graph_access_file

class Graph_network(Graph_AL):
    def __init__(self, source: str ,site:str) -> None:
        # ilay source eto efa ilay ip no node
        super().__init__(source)
        self.modified =True
        self.list_paths =None
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

    def cut_path(self , node1 ,node2 ,both_ways:bool):
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
