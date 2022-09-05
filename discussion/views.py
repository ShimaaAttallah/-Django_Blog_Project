from unicodedata import category
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .helper import send_forget_password_mail


from .models import Category, Comment, Post, Reply

# Create your views here.

def postview(request,id):
    post=get_object_or_404(Post,pk=id)
    categories=Category.objects.all()
    print(post.commentpost.all)
    if request.user in post.like.all():
        print('ssssssssssss')
    
    return render(request,'discussion/post.html',{'title':'my title','post':post,'categories':categories,'comments':post.commentpost.all().order_by('-createdat')})
@login_required
def likepost(request,id):
    post=get_object_or_404(Post,pk=id)
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        messages.success(request, post.title + " has been removed from your WishList")
    else:
        post.like.add(request.user)
        messages.success(request, "Added " + post.title + " to your WishList") 
        
    return HttpResponseRedirect(request.META["HTTP_REFERER"])       
   
@login_required
def unlikepost(request,id):
    post=get_object_or_404(Post,pk=id)
    if post.unlike.filter(id=request.user.id).exists():
        post.unlike.remove(request.user)
    else:
        post.unlike.add(request.user)
        
    return HttpResponseRedirect(request.META["HTTP_REFERER"])       
       
class AddComment(LoginRequiredMixin,CreateView):
    
    model=Comment
    fields=('content',)
    template_name='discussion/addcomment.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post=get_object_or_404(Post,pk=self.kwargs['id'])
        return super().form_valid(form)
    def get_context_data(self,*args, **kwargs):
        context = super(AddComment, self).get_context_data(*args,**kwargs)
        context['categories'] = Category.objects.all()
        return context
    def get_success_url(self):
        return reverse('post', kwargs={'id':self.kwargs['id']})
    
class AddReply(LoginRequiredMixin,CreateView):
    
    model=Reply
    fields=('content',)
    template_name='discussion/addcomment.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.comment=get_object_or_404(Comment,pk=self.kwargs['id'])
        return super().form_valid(form)
    def get_context_data(self,*args, **kwargs):
        context = super(AddReply, self).get_context_data(*args,**kwargs)
        context['categories'] = Category.objects.all()
        return context
    def get_success_url(self):
        return reverse('post', kwargs={'id':self.object.comment.post.pk})
    
    
    
    
@login_required
def subscribe(request,id):
    category=get_object_or_404(Category,pk=id)
    if category.user.filter(id=request.user.id).exists():
        category.user.remove(request.user)
        message=f'you unsubscibe {category.name} in our website'
    else:
        category.user.add(request.user)
        message=f'you subscibe {category.name} in our website'
        
    try:
        send_forget_password_mail(request.user.email, message)
    except Exception:
        pass
    return HttpResponseRedirect(request.META["HTTP_REFERER"])       


@login_required
def home(request):
    # posts = Post.objects.order_by('-createdat')
    posts = Post.objects.filter(category__user=request.user).order_by('-createdat')
    category=  Category.objects.all()
    paginator = Paginator(posts,1) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'discussion/home.html', context={"posts": posts,'categories':category,'page_obj': page_obj})  


      
def searchPost(request):
    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title=searched)
        categories = Post.objects.filter(category__name=searched)
        category=  Category.objects.all()
        context = {'searched':searched, 'posts':posts,'categories':category,'categoriess':categories}
        
        return render(request, 'discussion/search.html',context)
    else:
        
        return render(request, 'discussion/search.html')