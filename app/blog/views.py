from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


# Create your views here.
from .models import BlogPost
from blog.forms import BlogPostForm
from blog.forms import BlogPostModelForm


def blog_post_detail_page(request, slug):
    print("DJANGO SAYS: ", request.method, request.path, request.user)
    # queryset = BlogPost.objects.filter(slug=slug)
    # if queryset.count() == 0:
    #     raise Http404
    # else:
    #     obj = queryset.first()

    obj = get_object_or_404(BlogPost, slug=slug)

    template_name = 'blog_post_detail.html'
    context = {"object": obj}
    return render(request, template_name, context)


# Create Retrieve Update Delete


def blog_post_list_view(request):
    # list out objects
    # could be search
    now = timezone.now()
    qs = BlogPost.objects.all().published()
    print(qs)
    if request.user.is_authenticated:
        qs = BlogPost.objects.filter(user=request.user)
    template_name = 'blog/list.html'
    context = {'objects_list': qs}
    return render(request, template_name, context)


# @login_required
@staff_member_required
def blog_post_create_view(request):
    # create objects
    # ? use a form

    form = BlogPostModelForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = BlogPostModelForm()

    template_name = 'form.html'

    context = {
        'title': 'Create Post',
        'form': form
    }
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    # 1 object -> detail view
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/detail.html'
    context = {'object': obj}
    return render(request, template_name, context)


@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj.save()
    template_name = 'form.html'
    context = {"title": f"Update {obj.title}", 'form': form, }
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = 'blog/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/blog")
    context = {'object': obj}
    return render(request, template_name, context)
