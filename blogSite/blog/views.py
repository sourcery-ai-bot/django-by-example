from .models import Post, Comment
from .forms import (
    EmailPostForm,
    CommentForm,
    SearchForm,
)

from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
#from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from taggit.models import Tag


# Class Based View
#class PostListView(ListView):
#    queryset = Post.published.all()
#    context_object_name = 'posts'
#    paginate_by = 4
#    template_name = 'blog/post/list.html'

# Function Based View
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliever last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {
                      'page': page,
                      'posts': posts,
                      'tag': tag
                  })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similiar posts
    post_tags_id = post.tags.values_list('id', flat=True)
    similiar_posts = Post.published.filter(tags__in=post_tags_id) \
                                   .exclude(id=post.id)
    similiar_posts = similiar_posts.annotate(same_tags=Count('tags')) \
                                   .order_by('-same_tags', '-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {
                      'comments': comments,
                      'comment_form': comment_form,
                      'new_comment': new_comment,
                      'post': post,
                      'similiar_posts': similiar_posts,
                  })


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'body'),
            ).filter(search=query)
    return render(request,
                  'blog/post.search.html',
                  {
                      'form': form,
                      'query': query,
                      'results': results
                  })


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,
                             id=post_id,
                             status='published')

    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                        post.get_absolute_url())
            subject = f'{cd["name"]} ({cd["email"]}) recommends you read "{post.title}"'
            message = f'Read "{post.title}" at {post_url}\n\n{cd["name"]}\'s comments {cd["comments"]}'
            send_mail(subject, message, 'info@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,
                  'blog/post/share.html',
                  {
                      'form': form,
                      'post': post,
                      'sent': sent,
                  })

