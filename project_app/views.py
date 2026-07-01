from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Blog, Comment

User = get_user_model()
def homepage(request):
    return render(request,'base.html')

def register(request):
    if request.method == 'POST':
        if User.objects.filter(username=request.POST['username']).exists():
            return render(request, 'register.html', {'error': 'Username exists'})

        user = User.objects.create_user(
            username=request.POST['username'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            contact_number=request.POST['contact'],
            password=request.POST['password']
        )

        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
            user.save()

        return redirect('login')

    return render(request, 'register.html')



def user_login(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('blog_list')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')



@login_required
def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.contact_number = request.POST['contact']

        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()
        return redirect('profile')

    return render(request, 'profile.html')



@login_required
def blog_list(request):
    search = request.GET.get('search', '')
    blogs = Blog.objects.filter(
        Q(title__icontains=search) | Q(content__icontains=search)
    ).order_by('-created_at')

    paginator = Paginator(blogs, 5)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)

    return render(request, 'blog_list.html', {'blogs': blogs})



@login_required
def blog_create(request):
    if request.method == 'POST':
        Blog.objects.create(
            user=request.user,
            title=request.POST['title'],
            content=request.POST['content'],
            image=request.FILES.get('image')
        )
        return redirect('blog_list')

    return render(request, 'blog_create.html')



@login_required
def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = Comment.objects.filter(blog=blog).order_by('-created_at')

    if request.method == 'POST':
        # PREVENT AUTHOR FROM COMMENTING
        if request.user == blog.user:
            return redirect('blog_detail', id=blog.id)

        Comment.objects.create(
            blog=blog,
            user=request.user,
            comment=request.POST.get('comment')
        )
        return redirect('blog_detail', id=blog.id)

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'comments': comments
    })


@login_required
def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id, user=request.user)
    blog.delete()
    return redirect('blog_list')

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)


    if comment.user == request.user:
        blog_id = comment.blog.id
        comment.delete()
        return redirect('blog_detail', blog_id)

    return redirect('blog_detail', comment.blog.id)