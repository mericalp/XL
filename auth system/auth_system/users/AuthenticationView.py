from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q
from .forms import SignInForm, SignupForm, UserInfoUpdate, UpdatePass
from .tokens import account_activation_token

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class AuthenticationView(View):
    action_map = {
        'login': {'admin': 'get_admin_login', 'employee': 'get_employee_login'},
        'signup': {'admin': 'get_admin_signup', 'employee': 'get_employee_signup'},
        'profile': ('get_profile', 'post_profile'),
        'reset_password': ('get_reset', 'post_reset'),
        'change_password': ('get_change', 'post_change'),
        'activate': ('get_activate', None),
        'logout': ('get_logout', None)
    }

    def dispatch(self, request, action=None, type=None, *args, **kwargs):
        self.action = action
        self.type = type

        if action in ['login', 'signup']:
            # Validate type for login and signup
            if not type or type not in self.action_map[action]:
                return redirect('employee_login')  # Default redirection
            handler = getattr(self, self.action_map[action][type])
        else:
            # Handle other actions (profile, reset_password, etc.)
            if not action in self.action_map:
                return redirect('login')
            handler = getattr(self, self.action_map[action][0] if request.method == 'GET' else self.action_map[action][1])
        
        return handler(request, *args, **kwargs)

    # Admin login view
    def get_admin_login(self, request):
        if request.user.is_authenticated and request.user.status == 'admin':
            return redirect('admin_dashboard')  # Replace with admin dashboard
        return render(request, 'admin_login.html', {'form': SignInForm()})

    # Employee login view
    
    def get_employee_login(self, request):
        if request.user.is_authenticated and request.user.status == 'regular':
            return redirect('attendance_view')  # Replace with employee dashboard
        return render(request, 'login.html', {'form': SignInForm()})

    # Admin signup view
    def get_admin_signup(self, request):
        
        if request.user.is_authenticated and request.user.status == 'admin':
            return redirect('admin_login')
        return render(request, 'admin_register.html', {'form': SignupForm()})

    # Employee signup view
    def get_employee_signup(self, request):
        
        if request.user.is_authenticated and request.user.status == 'employee':
            return redirect('login')
        return render(request, 'register.html', {'form': SignupForm()})



    @method_decorator(login_required)
    def get_profile(self, request, username):
        user = get_user_model().objects.filter(username=username).first()
        if not user:
            return redirect('profile')
        form = UserInfoUpdate(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(request, 'profile.html', {'form': form})

    @method_decorator(login_required)
    def post_profile(self, request, username):
        form = UserInfoUpdate(request.POST, request.FILES, instance=request.user)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'profile.html', {'form': form})

        user_form = form.save()
        messages.success(request, f'{user_form.username}, Profiliniz güncellendi!')
        return redirect('profile', user_form.username)

    def get_reset(self, request):
        return render(request, 'reset_the_pass.html', {'form': PassResetForm()})

    def post_reset(self, request):
        form = PassResetForm(request.POST)
        if not form.is_valid():
            for key, error in form.errors.items():
               #  if key == 'captcha' and error[0] == 'Bu alan gereklidir.':
               #      messages.error(request, "reCAPTCHA testini geçmelisiniz")
                    continue
            return render(request, 'reset_the_pass.html', {'form': form})

        email = form.cleaned_data['email']
        user = get_user_model().objects.filter(Q(email=email)).first()
        if user:
            self.send_reset_email(request, user)
            messages.success(request, "Şifre sıfırlama e-postası gönderildi")
        return redirect('homepage')

    @method_decorator(login_required)
    def get_change(self, request):
        return render(request, 'reset_the_pass_confirm.html', 
                     {'form': UpdatePass(request.user)})

    @method_decorator(login_required)
    def post_change(self, request):
        form = UpdatePass(request.user, request.POST)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'reset_the_pass_confirm.html', {'form': form})

        form.save()
        messages.success(request, "Şifreniz değiştirildi")
        return redirect('login')

    def get_activate(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, "Giriş yapabilirsiniz")
            else:
                messages.error(request, "Link geçersiz")
        except:
            messages.error(request, "Link geçersiz")
        return redirect('login')

    @method_decorator(login_required)
    def get_logout(self, request):
         logout(request)
         messages.info(request, "Çıkış yapıldı!")
         return redirect('login')

    def send_activation_email(self, request, user):
        subject = "Hesabını Aktif Et"
        message = render_to_string("account_activat_temp.html", {
            'user': user.username,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        })
        email = EmailMessage(subject, message, to=[user.email])
        if email.send():
            messages.success(request, f'Sayın {user}, email adresinizi kontrol edin')
        else:
            messages.error(request, f'Email gönderilemedi {user.email}')

    def send_reset_email(self, request, user):
        subject = "Şifre Sıfırlama İsteği"
        message = render_to_string("reset_the_pass_temp.html", {
            'user': user,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        })
        return EmailMessage(subject, message, to=[user.email]).send()