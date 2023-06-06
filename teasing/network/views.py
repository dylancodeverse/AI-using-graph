import base64
import os
import time
from django.conf import settings
from django.shortcuts import render
from .models_custom.network.Graph_network import Graph_network
from django.views.decorators.cache import never_cache
from .models_custom.network.Graph_network import Graph
from django.core.files import File


def index(request):
    return render(request ,'network/network.html')

@never_cache
def initialize_graph(request):
    if request.method == 'POST':
        graph_file = request.FILES.get('graph-file')
        url_mapping_file = request.FILES.get('url-mapping-file')

        if graph_file and url_mapping_file:
            graph_file_path = handle_uploaded_file(graph_file, graph_file.name)
            url_mapping_file_path = handle_uploaded_file(url_mapping_file, url_mapping_file.name)

            a = Graph_network(graph_file_path, url_mapping_file_path)
            
            image_path = a.prepare_image()
            request.session['graph_file_path'] = graph_file_path
            request.session['url_mapping_file_path'] = url_mapping_file_path

            return render(request, 'network/success.html', context={'link': image_path})

    return render(request, 'your_template.html')

def cut_path(request):
    if request.method == 'POST':
        node1 = request.POST.get('node1').strip()
        node2 = request.POST.get('node2').strip()
        select = request.POST.get('select')
        
        if select == 'true':
            select = True
        else:
            select = False
            
        graph_file_path = request.session.get('graph_file_path')
        url_mapping_file_path = request.session.get('url_mapping_file_path')
        a = Graph_network(graph_file_path, url_mapping_file_path)
        print(select)
        a.cut_path(node1, node2, select)
        
        image_path = a.prepare_image()
        return render(request, 'network/success.html', context={'link': image_path})

    return render(request, 'your_template.html')



def request_domain(request):
    graph_file_path = request.session.get('graph_file_path')
    url_mapping_file_path = request.session.get('url_mapping_file_path')
    domain = request.POST.get('domain')
    ip = request.POST.get('ip')
    graph = Graph_network(graph_file_path, url_mapping_file_path)
    response = graph.get_path(ip, domain)
    
    return render(request, 'network/result_search.html', {'response': response})










def handle_uploaded_file(f, filename):
    destination = os.path.join(settings.UPLOADS_DIR, filename)
    with open(destination, 'wb') as destination_file:
        for chunk in f.chunks():
            destination_file.write(chunk)
    return destination
