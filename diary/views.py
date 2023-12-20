from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, RecommendedMusic
from django.core.exceptions import PermissionDenied
from recommend import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

##@login_required
@method_decorator(login_required, name='dispatch')
class PostList(ListView):
    model = Post
    template_name = 'diary/home.html'
    ordering = '-pk'
    def get_queryset(self):
        # 현재 로그인한 사용자와 게시글 작성자가 동일한 게시글만 필터링하여 반환
        return Post.objects.filter(author=self.request.user)

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

import json

def report(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = post.content
    title = post.title
    emotion = max_score_show(content)

    # 추천 함수 호출 및 음악 추천 데이터 받아오기
    re_sys = recommend(content)
    first_music = re_sys[0][1]+'-'+re_sys[0][2]
    second_music = re_sys[1][1]+'-'+re_sys[1][2]
    third_music = re_sys[2][1]+'-'+re_sys[2][2]
    fourth_music = re_sys[3][1]+'-'+re_sys[3][2]

    # 음악 추천 데이터 저장
    save_recommended_music(re_sys)

    # get_recommended_music_list 함수 호출하여 추천 음악 리스트 가져오기
    recommended_music_list = get_recommended_music_list(request)

    # 그래프 데이터 생성
    score = senti_score(content)
    score_json = json.dumps(score)  # JSON 형식으로 변환

    # 음악 추천에 따른 그래프 생성
    first_graph = first_music_graph(content)
    second_graph = second_music_graph(content)
    third_graph = third_music_graph(content)
    fourth_graph = fourth_music_graph(content)

    return render(
        request,
        'diary/recommend.html',
        {
            'post': post,
            'content': content,
            'title': title,
            'emotion': emotion,
            're_sys': re_sys,  # 음악 추천 데이터 전달
            'recommended_music_list': recommended_music_list,
            'first_music': first_music,
            'second_music': second_music,
            'third_music': third_music,
            'fourth_music': fourth_music,
            'score_json': score_json,  # JSON 형식의 그래프 데이터 전달
            'first_graph': first_graph.to_json(),
            'second_graph': second_graph.to_json(),
            'third_graph': third_graph.to_json(),
            'fourth_graph': fourth_graph.to_json(),
        }
    )


def save_recommended_music(data_list):
    for music_data in data_list:
        # 이미 저장된 음악인지 확인
        existing_music = RecommendedMusic.objects.filter(artist=music_data['artist'], title=music_data['title']).exists()
        if not existing_music:
            music = RecommendedMusic.objects.create(
                title=music_data['title'],
                artist=music_data['artist'],
            )
            music.save()


# def get_recommended_music_list(request):
#     recommended_music_list = []
#
#     # 현재 로그인한 사용자가 작성한 게시글에 대한 추천 음악 가져오기
#     user_posts = Post.objects.filter(author=request.user)
#
#     # 작성한 게시글의 제목 가져오기
#     user_post_titles = user_posts.values_list('title', flat=True)
#
#     # 작성한 게시글 제목을 기준으로 추천 음악 가져오기
#     recommended_music = set(RecommendedMusic.objects.filter(title__in=user_post_titles))
#
#     for music in recommended_music:
#         recommended_music_list.append(f"{music.artist} - {music.title}")
#
#     return render(
#         request,
#         'diary/playlist.html',
#         {'recommended_music': recommended_music_list}
#     )

def get_recommended_music_list(request):
    user_posts = Post.objects.filter(author=request.user)
    user_post_titles = user_posts.values_list('title', flat=True)

    recommended_music = RecommendedMusic.objects.filter(title__in=user_post_titles)

    recommended_music_list = []
    for music in recommended_music:
        recommended_music_list.append(f"{music.artist} - {music.title}")

    return recommended_music_list
