from django.views import generic
from .forms import LoginForm
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect,render,resolve_url
from django.template.loader import get_template
from django.views import generic
from .forms import (
    MyPasswordChangeForm,MySetPasswordForm,LoginForm, UserCreateForm, UserUpdateForm,MyPasswordResetForm,MyPasswordResetForm
)


User = get_user_model()

def user_delete_confirm(request):
    return render(request,"account/user_delete_confirm.html")

def user_delete(request,user_pk):
    req_user=request.user
    user=User.objects.get(pk=user_pk)
    if req_user.pk == user.pk or req_user.is_superuser:
        user.delete()
        return render(request,"tabilog/delete_complete.html")
    else:
        return HttpResponseRedirect("/")

class Top(generic.TemplateView):
    template_name = 'top.html'


class Login(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

class Logout(LoginRequiredMixin, LogoutView):
    template_name = 'top.html'

class UserCreate(generic.CreateView):
    template_name = 'account/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'username': user.nickname,
        }


        message_template = get_template('mail_template/create/message.txt')
        message = message_template.render(context)

        user.notify_user("Trippp本登録のお願い", message)
        return redirect('account:user_create_done')

class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'account/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'account/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoenNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = False

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class UserDetail(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = 'account/mypage.html'


class UserUpdate(OnlyYouMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'account/user_form.html'

    def get_success_url(self):
        return resolve_url('account:mypage', pk=self.kwargs['pk'])

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change.html'

class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'account/password_change_done.html'

class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'mail_template/reset/subject.txt'
    email_template_name = 'mail_template/reset/message.txt'
    template_name = 'account/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('account:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('account:password_reset_complete')
    template_name = 'account/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'accoumt/password_reset_complete.html'
