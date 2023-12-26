from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from autoslug.utils import slugify
from accounts.models import Profile
from accounts import groups, permissions
from blog.models import Post

# Create your views here.
class Home(View):
    def get(self, request, *args, **kwargs):
        # user_profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(tag='fr')

        context = {
            'posts': posts[0:4]
        }
        return render(request, 'blog/home.html', context=context)

@method_decorator(login_required, name='dispatch')
class AddPost(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/add_post.html')
    
    def post(self, request, *args, **kwargs):
        owner = Profile.objects.get(user=request.user)
        plan = owner.plan
        post_title = request.POST['title']
        post_content = request.POST['content']

        new_post = Post.objects.create(
            owner_profile=owner,
            title=post_title,
            content=post_content,
            tag=plan
        )

        print(f'New {new_post.get_tag_display()} post created.')
        return redirect('blog:view-posts')

# @method_decorator(login_required, name='dispatch')
class ViewPost(View):

    def get(self, request, post_slug, *args, **kwargs):
        post = get_object_or_404(Post, slug_title=post_slug)
        
        if request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=request.user)
            user_has_perm = permissions.check_permissions(user=request.user, tag=post.tag)
        
            if user_has_perm:
                context = {
                    'post': post,
                    'profile': profile
                }
                return render(request, 'blog/view_post.html', context=context)
            else:
                print('Permission Denied')
                return redirect('blog:home')
            
        else:
            if post.tag == 'fr':
                context = {
                    'post': post
                }
                return render(request, 'blog/view_post.html', context=context)

@method_decorator(login_required, name='dispatch')
class UpdatePost(View):
    def get(self, request, post_slug, *args, **kwargs):
        post = get_object_or_404(Post, slug_title=post_slug)
        profile = get_object_or_404(Profile, user=request.user)
    
        if post.owner_profile != profile:
            print('Permission Denied')
            return redirect('accounts:home')
        else:
            context = {
                'post': post,
                'profile': profile
            }
            return render(request, 'blog/update_post.html', context=context)

    def post(self, request, post_slug, *args, **kwargs):
        owner = get_object_or_404(Profile, user=request.user)
        post = get_object_or_404(Post, owner_profile=owner, slug_title=post_slug)
        
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.slug_title = slugify(post.title)

        post.save(update_fields=[
            'title',
            'content',
            'slug_title'
        ])

        print('Post Updated')
        return redirect('blog:view-post', post_slug=post.slug_title)
    
@method_decorator(login_required, name='dispatch')
class ViewPosts(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        posts = Post.objects.filter(tag__in=profile.get_ranks())
        context = {
            'posts': posts,
            'profile': profile
        }

        return render(request, 'blog/all_posts.html', context=context)

home = Home.as_view()
add_post = AddPost.as_view()
view_post = ViewPost.as_view()
update_post = UpdatePost.as_view()
view_posts = ViewPosts.as_view()