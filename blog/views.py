from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, HashTag
from django.utils import timezone
from .forms import BlogForm, CommentForm

# Create your views here.


def home(request):
    blog = Blog.objects  # 쿼리셋
    return render(request, "home.html", {"blogs": blog})  # blogs라는 이름으로 blog를 전달할거야

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    blog_hashtag = blog_detail.hashtag.all()
    return render(
        request, "detail.html", {"blog": blog_detail, 'hashtags': blog_hashtag}
    )  # blog라는 이름으로 blog_detail을 전달할거야

def new(request):
    form = BlogForm()
    return render(request, "new.html", {"form": form})

def create(request):
    new_form = BlogForm(request.POST, request.FILES)  # post->file형태로 뉴폼에 저장하겠다
    if new_form.is_valid():  # 유효성 검사
        new_blog = new_form.save(commit=False)  # 잠깐 임시저장
        new_blog.pub_date = timezone.now()  # 현재 시간으로 저장
        new_blog.save()
        hashtags = request.POST['hashtags']
        hashtag = hashtags.split(",")
        for tag in hashtag:
            ht = HashTag.objects.get_or_create(hashtag_name=tag) 
            new_blog.hashtag.add(ht[0])
            # 실행이 잘됐다면 - 방금 저장한 아이를 디테일뷰로 보겠어
        # 유효하다면 뉴블로그에 저장해
    return redirect("home")

def edit(request, blog_id):  # 수정되기 전 블로그
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, "edit.html", {"blog": blog_detail})

def update(request, blog_id):  # 수정된 블로그
    blog_update = get_object_or_404(Blog, pk=blog_id)
    blog_update.title = request.POST["title"]
    blog_update.contents = request.POST["contents"]
    blog_update.save()
    return redirect("home")

def delete(request, blog_id):
    blog_delete = get_object_or_404(Blog, pk=blog_id)
    blog_delete.delete()
    return redirect("home")

def add_comment_to_post(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid(): #유효성 검사
            comment = form.save(commit=False)
            comment.post = blog
            comment.save()
            return redirect('detail', blog_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment_to_post.html', {'form' : form}) #form이라는 이름으로 넘겨줌

