from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Response, Subscriptions, Category
from datetime import datetime
from .forms import PostForm, ResponseForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .filters import PostFilter, ResponseFilter
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

class PostView(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 4  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        return context
   # Переопределяем функцию получения списка товаров

class PostDetail(DetailView):
    raise_exception = True
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        form = ResponseForm()
        post = get_object_or_404(Post, pk=pk)
        responses = post.reply.all()
        context['post'] = post
        context['responses'] = responses
        context['form'] = form
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit = False)
        post.author=self.request.user
        post.save()
        return super().form_valid(form)

class PostEdit(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ResponseCreate(LoginRequiredMixin, CreateView):
    permission_required = ('PostBoard_main.add_response')
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_create.html'
    # success_url = res_post.get_absolute_url()

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            form = ResponseForm(request.POST or None)
            post_to_res = get_object_or_404(Post, id=pk)
            if form.is_valid():
                f = form.save(commit=False)
                f.res_user_id = self.request.user.id
                f.res_post_id = post_to_res.id
                form.save()
                return super().form_valid(form)
            else:
                return render(request, 'posts/response_create.html', {'form': form})
        else:
            form = ResponseForm()
            return render(request, 'posts/response_create.html', {'form': form})


class ResponseDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('PostBoard_main.delete_response')
    raise_exception = True
    model = Response
    template_name = 'response_delete.html'
    # success_url = reverse_lazy('posts')
    # success_url = redirect('posts:post_detail')

    def get_success_url(self):
        return self.request.GET.get('next', reverse('posts'))

# def to_response_delete(request, pk):
#     # response = get_object_or_404(Response, pk=id)
#     response = Response.objects.filter(id=request.POST.get('id'))
#     response.delete()
#     return redirect('responses')


class ResponseAccept(PermissionRequiredMixin, UpdateView):
    permission_required = ('PostBoard_main.change_response')
    raise_exception = True
    form_class = ResponseForm
    model = Response
    template_name = 'response_accept.html'

    def post(self, request, pk, **kwargs):
        if request.method == 'POST':
            resp = Response.objects.get(id=pk)
            resp.status = True
            resp.save()
            return redirect(f'responses')
        else:
            return redirect(f'responses')

    # def get_success_url(self):
    #     return self.request.GET.get('next', reverse('posts'))
class ResponseList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Response
    ordering = '-time_in'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 20

    def get_queryset(self):
        queryset = Response.objects.filter(res_post__user=self.request.user.id).order_by('-time_in')
        self.filterset = ResponseFilter(self.request.GET, queryset, request=self.request.user.id)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['time_in'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context

@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='Зарегистрированные пользователи')
    if not user.groups.filter(name='Зарегистрированные пользователи').exists():
        group.user_set.add(user)
        #RegUsers.objects.create(reg_user=user)
    return redirect('posts')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)

        action = request.POST.get('action')
        if action == 'subscribe':
            Subscriptions.objects.create(user=request.user, to_category=category)
        elif action == 'unsubscribe':
            Subscriptions.objects.filter(
                user=request.user,
                to_category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriptions.objects.filter(
                user=request.user,
                to_category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
