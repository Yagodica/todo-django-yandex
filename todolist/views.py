# views.py
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from .models import ToDo
from datetime import datetime

def index(request):
    todos = ToDo.objects.all()
    return render(request, 'todoapp/index.html', {'todo_list': todos, 'title': 'Главная страница'})

@require_http_methods(['POST'])
def add(request):
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    expiration_time = request.POST.get('expiration_time', '')
    if title:
        todo = ToDo(title=title, description=description, expiration_time=expiration_time)
        todo.save()
        messages.success(request, 'To-do item added successfully.')
    else:
        messages.error(request, 'Title cannot be empty.')
    return redirect('index')

def update(request, todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id)
        todo.is_complete = not todo.is_complete
        todo.save()
        return JsonResponse({'is_complete': todo.is_complete})
    except ToDo.DoesNotExist:
        return JsonResponse({'error': 'To-do item does not exist.'}, status=404)

@require_http_methods(['POST'])
def edit(request, todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id)
        todo.title = request.POST.get('title', '').strip()
        todo.description = request.POST.get('description', '').strip()
        todo.expiration_time = request.POST.get('expiration_time', '')
        todo.save()
        return JsonResponse({'success': True})
    except ToDo.DoesNotExist:
        return JsonResponse({'error': 'To-do item does not exist.'}, status=404)

def delete(request, todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id)
        todo.delete()
        messages.success(request, 'To-do item deleted successfully.')
    except ToDo.DoesNotExist:
        messages.error(request, 'To-do item does not exist.')
    return redirect('index')
