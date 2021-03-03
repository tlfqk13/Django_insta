from django.http import JsonResponse, response
from django.views import View
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.core.validators import validate_email,ValidationError
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required

from contents.models import Content,Image,FollowRelation


# BaseView를 만들꺼다
class BaseView(View):
    @staticmethod
    def response(data={},message='',status=200):
        result={
            'data':data,
            'message':message,
        }
        return JsonResponse(result,status=status)


class UserCreateView(BaseView):
    @method_decorator
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView,self).dispatch(request,*args,**kwargs)
    
    def post(self,request):
        username=request.POST.get('username','')
        if not username:
            return self.response(message='아이디를 입력해주세요.',status=400)
        password=request.POST.get('password','')
        if not password:
            return self.password(message='페스워드를 입력해주세요.',status=400)
        email=request.POST.get('email','')
        if not email:
            try: 
                validate_email(email)
            except ValidationError:
                self.response(message='올바른 이메일을 입력해주세요.',status=400)
        
        try:
            user=User.objects.create_user(username,email,password)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.',status=400)

        return self.response({'user.id':user.id})


class UserLoginView(BaseView):
    def post(self,request):
        username=request.POST.get('username','')
        if not username:
            return self.response(message='아이디를 입력해주세요',status=400)
        password=request.POST.get('password','')
        if not password:
            return self.response(message='패스워드를 입력해주세요',status=400)
        
        user=authenticate(request,username=username,password=password)
        if user is None:
            return self.response(message='입력 정볼르 확인해주세요',status=400)
        login(request,user)

        return self.response()

class UserLogoutView(BaseView):
    def get(self,request):
        logout(request)
        return self.response()

class ContentCreateView(BaseView):
    def post(self,request):
        text=request.POST.get('text','').strip()
        content=Content.objects.create(user=request.user,text=text)
        for idx, file in enumerate(request.FILES.values()):
            Image.objects.create(content=content,image=file,order=idx)
        return self.response({})

