from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView, View, TemplateView,DeleteView
from App_Blog.models import Blog, Comment
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from App_Blog.forms import CommentForm
import uuid
# Create your views here.

class MyBlogs(LoginRequiredMixin, TemplateView):
    template_name = 'App_Blog/my_blogs.html'

class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'App_Blog/create_blog.html'
    fields = ('blog_title', 'blog_content', 'blog_image',)

    def form_valid(self,form):
        blog_obj = form.save(commit=False)
        blog_obj.author = self.request.user
        title = blog_obj.blog_title
        blog_obj.slug = title.replace(" ", "-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))

class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'App_Blog/blog_list.html'

@login_required
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug' : slug}))
    return render(request, 'App_Blog/blog_details.html', context={'blog': blog, 'comment_form':comment_form})
