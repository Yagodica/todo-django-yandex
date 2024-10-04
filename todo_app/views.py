# todo_app/views.py
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .models import ToDoItem, ToDoList

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


class ListListView(LoginRequiredMixin, ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)


class ItemListView(LoginRequiredMixin, ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"], todo_list__user=self.request.user)

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"], user=self.request.user)
        return context


class ListCreate(LoginRequiredMixin, CreateView):
    model = ToDoList
    fields = ["title"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self):
        context = super().get_context_data()
        context["title"] = "Add a new list"
        return context


class ItemCreate(LoginRequiredMixin, CreateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_initial(self):
        initial_data = super().get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"], user=self.request.user)
        initial_data["todo_list"] = todo_list
        return initial_data

    def get_context_data(self):
        context = super().get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"], user=self.request.user)
        context["todo_list"] = todo_list
        context["title"] = "Create a new item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])
    

class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date",
    ]

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit item"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])


class ListDelete(LoginRequiredMixin, DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index")



class ItemDelete(LoginRequiredMixin, DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
    

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login')