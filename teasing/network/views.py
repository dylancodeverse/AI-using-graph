import os
from django.conf import settings
from django.shortcuts import render
from .models_custom.network.Graph_network import Graph_network
def index(request):
    a= Graph_network("/home/dylan/Desktop/Mr_Tsinjo/Text File.txt" ,"/home/dylan/Desktop/Mr_Tsinjo/domaines.txt")
    print(a.adjancy_list)
    
    return render(request ,'network/network.html')


def initialize_graph(request):
    if request.method == 'POST':
        graph_file = request.FILES.get('graph-file')
        url_mapping_file = request.FILES.get('url-mapping-file')
        
        if graph_file and url_mapping_file:
            graph_file_path = handle_uploaded_file(graph_file, graph_file.name)
            url_mapping_file_path = handle_uploaded_file(url_mapping_file, url_mapping_file.name)
            a = Graph_network(graph_file_path, url_mapping_file_path)
            print(a)

            # Redirigez ou affichez une réponse appropriée
            return render(request, 'network/success.html')
    
    return render(request, 'your_template.html')


def handle_uploaded_file(f, filename):

    
    destination = os.path.join(settings.UPLOADS_DIR, filename)
    with open(destination, 'wb') as destination_file:
        for chunk in f.chunks():
            destination_file.write(chunk)
    return destination
