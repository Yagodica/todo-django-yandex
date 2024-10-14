from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import ToDo


@login_required
def index(request):
    todos = ToDo.objects.filter(user=request.user)
    return render(request, 'todoapp/index.html', {'todo_list': todos, 'title': 'Главная страница'})

@require_http_methods(['POST'])
@login_required
def add(request):
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    deadline = request.POST.get('deadline', '')
    if title:
        todo = ToDo(title=title, description=description, deadline=deadline, user=request.user)
        todo.save()
        messages.success(request, 'To-do item added successfully.')
    else:
        messages.error(request, 'Title cannot be empty.')
    return redirect('index')

@login_required
def update(request, todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id, user=request.user)
        todo.is_complete = not todo.is_complete
        todo.save()
        return JsonResponse({'is_complete': todo.is_complete})
    except ToDo.DoesNotExist:
        return JsonResponse({'error': 'To-do item does not exist.'}, status=404)

@require_http_methods(['POST'])
@login_required
def edit(request, todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id, user=request.user)
        todo.title = request.POST.get('title', '').strip()
        todo.description = request.POST.get('description', '').strip()
        todo.deadline = request.POST.get('deadline', '')
        todo.save()
        return JsonResponse({'success': True})
    except ToDo.DoesNotExist:
        return JsonResponse({'error': 'To-do item does not exist.'}, status=404)

@login_required
def delete(request, todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id, user=request.user)
        todo.delete()
        messages.success(request, 'To-do item deleted successfully.')
    except ToDo.DoesNotExist:
        messages.error(request, 'To-do item does not exist.')
    return redirect('index')

@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return redirect('login')
