from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from .models import Post


class PostListView(ListView):
    '''
    Альтернативное представление списка постов
    '''
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(
        request,
        'blog/detail.html',
        {'post': post}
    )