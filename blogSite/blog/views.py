from .models import Post
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)

# Class Based View
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'

# Function Based View
#def post_list(request):
#    object_list = Post.published.all()
#    paginator = Paginator(object_list, 5) # 3 posts on each page
#    page = request.GET.get('page')
#    try:
#        posts = paginator.page(page)
#    except PageNotAnInteger:
#        # If page is not an integer deliver the first page
#        posts = paginator.page(1)
#    except EmptyPage:
#        # If page is out of range deliever last page of results
#        posts = paginator.page(paginator.num_pages)
#    return render(request,
#                  'blog/post/list.html',
#                  {
#                      'page': page,
#                      'posts': posts,
#                  })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

