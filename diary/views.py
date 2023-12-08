from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.core.exceptions import PermissionDenied
from recommend import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect

##@login_required
@method_decorator(login_required, name='dispatch')
class PostList(ListView):
    model = Post
    template_name = 'diary/home.html'
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']  # author 필드는 뷰에서 자동으로 설정될 것입니다.

    def form_valid(self, form):
        form.instance.author = self.request.user  # 현재 로그인한 사용자를 작성자로 설정
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    template_name = 'diary/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



@login_required
def create_post(request):
    if request.method == 'POST':
        # POST 요청에서 데이터 가져오기
        title = request.POST.get('title')
        content = request.POST.get('content')

        # 현재 로그인한 사용자를 작성자로 설정하여 새로운 게시글 생성
        new_post = Post.objects.create(
            title=title,
            content=content,
            author=request.user  # 현재 로그인한 사용자를 작성자로 지정
        )
        new_post.save()  # 변경 사항 저장

        # 게시글이 작성된 후 리다이렉트 또는 다른 작업 수행
        return redirect('post_detail', pk=new_post.pk)  # 새로 작성된 게시글 상세 페이지로 이동

    # GET 요청 시 필요한 작업 처리 (예: 게시글 작성 폼 표시)
    return render(request, 'diary/home.html')


def report(request):
    posts = Post.objects.only('content')
    content = posts.filter(pk=id)
    score = max_score_show(content)
    re_sys = recommend(content)
    graph = show_mygraph(content)
    music_graph = show_music_graph(content)
    return render(
        request,
        'diary/recommend.html',
        {
            'posts': posts,
            'content': content,
            'score': score,
            're_sys': re_sys,
            'graph': graph,
            'music_graph': music_graph,
        }
    )