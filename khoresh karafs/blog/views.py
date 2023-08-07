from django.db.models import F
from django.views.generic import DetailView, CreateView

from blog.models import Article

from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    queryset = Article.objects.filter(status='p')

    def render_to_response(self, context, **response_kwargs):
        self.object.views = F('views') + 1
        self.object.save()
        response = super().render_to_response(context, **response_kwargs)
        return response


class LoginMidMixin(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/article_create.html'
    fields = '__all__'

class ArticleCreateView(LoginMidMixin):
    model = Article
    template_name = 'blog/article_create.html'   
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = [
                'author', 'title', 'slug', 'body', 'status', 'category', 'is_premium'
            ]
            self.queryset = Article.objects.all()
        else:
            self.fields = [
                'title', 'slug', 'body', 'category', 'is_premium'
            ]
            self.queryset = Article.objects.all()
            for iterator.
            self.author=request.user
            self.status='d'
        return super(LoginMidMixin, self).dispatch(request, *args, **kwargs)