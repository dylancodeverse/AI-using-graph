import base64
import os
import time
from django.conf import settings
from django.shortcuts import render
from .models_custom.network.Graph_network import Graph_network
from django.views.decorators.cache import never_cache


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
            print("---------------------------------")
            print(image_path)
            # Obtenir le chemin relatif de l'image par rapport à la racine du dossier media


            # Renvoyer le chemin relatif pour l'affichage dans le template
            return render(request, 'network/success.html')

    return render(request, 'your_template.html')







def handle_uploaded_file(f, filename):
    destination = os.path.join(settings.UPLOADS_DIR, filename)
    with open(destination, 'wb') as destination_file:
        for chunk in f.chunks():
            destination_file.write(chunk)
    return destination
