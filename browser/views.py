from django.shortcuts import render, get_object_or_404
from itertools import chain
from django.views.generic import ListView
from posts.models import Post
from profiles.models import Profile
from django.db.models import Q
from django import forms
from posts.forms import PostModelForm, CommentModelForm



def create_browser_views(request):
    context = {}

    form = BrowserResults(request.Post or None, request.Comment or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author= Post.author()
        obj.author= author
        obj.save()
        form= BrowserResults(request()
    
    context['form'] = form

    return render(request, "post/results.html", context)



def detail_browser_view(request, slug):

    context ={}

    browser_post =get_object_or_404(BrowserPost, slug=slug)
    context['browser_post'] = browser_post

    return render(request, 'post/detail_browse.html', context)



def edit_browser_views(request, slug):
    context = {}

    browser_post =get_object_or_404(BrowserPost, slug=slug)
    if request.Post:
        form = UpdateBrowserResults(request.Post or None, request.Comment or None, instance=browser_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            browser_post = obj

        form= UpdateBrowserResults(request(
            initial= {
                "title": browser_post.content,
                "image": browser_post.image,
            }
        )
    
    context['form'] = form

    return render(request, "post/results.html", context)


def get_browser_queryset(query =None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = BrowserPost.objects.filter(
            Q(content_icontains=q)
            Q(image_icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    
    return list(set(queryset))



# class BrowserView(ListView):
#     template_name = 'browser/view.html'
#     paginate_by = 20
#     count = 0
    
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['count'] = self.count or 0
#         context['query'] = self.request.GET.get('q')
#         return context

#     def get_queryset(self):
#         request = self.request
#         query = request.GET.get('q', None)
        
#         if query is not None:
#             posts_results        = Post.objects.browser(query=query)
#             profiles_results     = Profile.objects.browser(query=query)
            
#             # combine querysets 
#             queryset_chain = chain(
#                     posts_results,
#                     profiles_results
#             )        
#             qs = sorted(queryset_chain, 
#                         key=lambda instance: instance.pk, 
#                         reverse=True)
#             self.count = len(qs) # since qs is actually a list
#             return qs
#         return Post.objects.none() # just an empty queryset as default

#         # return Post.objects.browser(query=query)