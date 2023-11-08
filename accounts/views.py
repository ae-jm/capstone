# from django.contrib import auth
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect

# def signup(request):
#     if request.method == 'POST':
#         if request.POST['password1'] == request.POST['password2']:
#             user = User.objects.create_user(
#                 username=request.POST['username'],
#                 password=request.POST['password1'],
#                 email=request.POST['email'],
#             )
#             auth.login(request, user)
#             return redirect('/home/')
#         return render(request, 'signup_form.html')
#     return render(request, 'signup_form.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.forms import UserForm
from accounts.forms import LoginView, LogoutView, CreateView
from diary.views import PostList
from diary.models import Post
from django.db.models import Count

login = LoginView.as_view(
    template_name="accounts/login_form.html"
)

logout = LogoutView.as_view(
    next_page='/'
)

@login_required  # 함수위에 씌워주면 로그인시에만 확인 가능
def mypage(request):
    return render(request, 'accounts/profile.html')

# def get_context_data(self, **kwargs):
#     context = super(PostList, self).get_context_data()
#     context['post_count'] = Post.objects.all()
#     return context



signup = CreateView.as_view(
    form_class=UserForm,
    success_url='/accounts/login/', # 회원가입시 login화면으로 ㄱㄱ
    template_name='accounts/signup_form.html',
)





