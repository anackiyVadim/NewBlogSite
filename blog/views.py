from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import Post, Category, PostPhoto, Comment, Profile, User
from django.db.models import Q
from .forms import PostForm, CommentForm, SubscribeForm, CombinedForm, RegisterForm, PostPhotoFormSet
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2 + count % 2
    return {'cats1': all[:half], 'cats2': all[half:]}


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    paginator = Paginator(posts, 4)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def post(request, title=None):
    post = get_object_or_404(Post, title=title)
    imgs = PostPhoto.objects.filter(post=post)
    comment = Comment.objects.filter(post=post).order_by("-published_date")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.published_date = now()
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post', title=title)
    else:
        form = CommentForm()
    context = {"post": post, 'imgs': imgs, 'comment': comment, 'form': form}
    context.update(get_categories())
    return render(request, 'blog/post.html', context)


def about(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/about.html', context)


def contact(request):
    context = {}
    context.update(get_categories())
    return render(request, 'blog/contact.html', context)


def category(request, name=None):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by("-published_date")
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {"posts": posts}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscribeForm = form.save(commit=False)
            subscribeForm.save()
            return index(request)
    context = {"form": form}
    context.update(get_categories())
    return render(request, 'blog/index.html', context)


# @login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        photo_form = PostPhotoFormSet(request.POST, request.FILES, prefix='photos')
        if form.is_valid() and photo_form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            photo_form.instance = post
            photo_form.save()
            form.save_m2m()
            return index(request)
    else:
        form = PostForm()
        photo_form = PostPhotoFormSet(prefix='photos')
    context = {"form": form, 'photo_form': photo_form}
    context.update(get_categories())
    return render(request, 'blog/create.html', context)


def profile(request, user=None):
    users = get_object_or_404(User, username=user)
    subUser = Profile.objects.filter(user=users)
    context = {'subUser': subUser, 'users': users}
    context.update(get_categories())
    return render(request, 'blog/profile.html', context)


def update_profile(request):
    subUser = Profile.objects.all()
    if request.method == 'POST':
        form = CombinedForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    else:
        form = CombinedForm(instance=request.user)
    context = {'form': form, 'subUser': subUser}
    context.update(get_categories())
    return render(request, 'blog/update_profile.html', context)


def registration_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return redirect('index')
    else:
        form = RegisterForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, 'blog/registration_user.html', context)
