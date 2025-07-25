from .models import Post

def latest_blog_posts(request):
    posts = Post.published.all().order_by('-publish')[:8]
    return {'latest_blog_posts': posts}
