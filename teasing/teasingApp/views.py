from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from .models_custom.teasingApp.Graph_Teasing import Graph_Teasing
from .models_custom.teasingApp.Teasing import Teasing

def initialize(request):
    request.session['current'] = {
        'matrix': [
            [1,2,3],
            [4,5,6],
            [7,8,0]
        ]
    }    
    return redirect('index')

def index(request):
    param = request.session.get('current')
    print(param)
    return render(request ,'teasingApp/Teasing.html' ,context=param )

def shuffle(request, shuffle_number):
    matrix = request.session.get('current')['matrix']
    current =Teasing(len(matrix[0]),len(matrix))
    current.matrix = matrix
    if current is not None:
        current.shuffle(int(shuffle_number))
        request.session['current'] = {'matrix': current.matrix}
        html = render_to_string('teasingApp/board.html', {'matrix': current.matrix})
        return JsonResponse({'success': True, 'html': html})

def solve(request):
    matrix = request.session.get('current')['matrix']
    current =Teasing(len(matrix[0]),len(matrix))
    current.matrix = matrix
    goal_matrix=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
    goal_teasing = Teasing(3,3)
    goal_teasing.matrix = goal_matrix
    if current is not None:
        graph_teasing = Graph_Teasing(current)
        all_moves= graph_teasing.solve_taquin(goal_teasing)
        schema_moves = current.get_list_of_result_move(all_moves)
        board_to_render=[]
        for schema in schema_moves :
            html = render_to_string('teasingApp/board.html', {'matrix': schema.matrix})
            board_to_render.append(html)
        response_data = {'success':True ,'boardArray': board_to_render}
        return JsonResponse(response_data)

        

    

