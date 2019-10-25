from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic

from .forms import PostForm
from .models import Post


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return redirect('notices')
        else:
            return render(request, 'posts/addpost.html', {'form': form})
            print('error')
    else:
        form = PostForm()
        return render(request, 'posts/addpost.html', {'form': form})
        # return redirect('addpost')


def post_delete(request, tag):
    obj = Post.objects.get(title=tag)
    obj.delete()
    return redirect('notices')


class PostList(generic.ListView):
    queryset = Post.objects.all().order_by('-created_on')
    template_name = 'posts/allpost.html'


class PostListStud(generic.ListView):
    queryset = Post.objects.all().order_by('-created_on')
    template_name = 'posts/allpost_student.html'
