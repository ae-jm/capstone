from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import UserForm, CustomUserChangeForm, LoginView, LogoutView, CreateView
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.views import LoginView
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from diary.models import Post
# from django.views.generic import CreateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from accounts.forms import CustomUserCreationForm


login = LoginView.as_view(
    template_name="accounts/login_form.html"
)

logout = LogoutView.as_view(
    next_page='/'
)

# class UserRegistrationView(CreateView):
#     model = get_user_model()
#     form_class = UserRegistrationForm
#     success_url = '/accounts/login/'

# class UserLoginView(LoginView):
#     template_name = "accounts/login_form.html"
#
#     def form_invalid(self, form):
#         messages.error(sefl.request, '로그인에 실패하셨습니다.', extra_tags='danger')
#         return super.form_invalid(form)


@login_required  # 함수위에 씌워주면 로그인시에만 확인 가능
def mypage(request):
    post = Post.objects.filter(author=request.user)
    post_count = post.count()
    return render(
        request,
        'accounts/profile.html',
        {
            'post': post,
            'post_count': post_count,
        }
    )

signup = CreateView.as_view(
    form_class=UserForm,
    success_url='/accounts/login/', # 회원가입시 login화면으로 ㄱㄱ
    template_name='accounts/signup_form.html',
)

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # form.save()를 통해 새로운 사용자가 생성되고 반환된다
            # 아래의 줄을 추가하여 확인할 수 있다
            print("회원가입 시 form.save() 호출됨")
            return HttpResponseRedirect('/accounts/login/')  # 원하는 리다이렉션 URL로 변경
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup_form.html', {'form': form})

# def signup(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username=form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('index')
#         else:
#             form = UserForm()
#         return render(request, 'accounts/signup_form.html', {'form': form})

def delete(request):
    user = request.user
    user.delete()
    return redirect('pages/index.html')

def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:mypage')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/update.html', context)

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, '비밀번호가 성공적으로 변경되셨습니다!')
            return redirect('accounts:mypage')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)

# class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
#     success_url = reverse_lazy('change_password')
#     template_name = 'accounts/change_password.html'  # 템플릿 위치 재정의
#     form_class = PasswordChangeForm  # 커스텀 폼 지정
#
#     def form_valid(self, form):  # 유효성 검사 성공 이후 로직 입력
#         messages.success(self.request, '암호를 변경했습니다.')  # 성공 메시지
#         return super().form_valid(form)  # 폼 검사 결과를 리턴해야한다.
#
# change_password = PasswordChangeView.as_view()

