from django_filters import FilterSet
from .models import Post, Response

# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
   class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'text': ['icontains'],
           # количество товаров должно быть больше или равно
           'categoryType': ['icontains'],
           'price': [
               'lt',  # цена должна быть меньше или равна указанной
               'gt',  # цена должна быть больше или равна указанной
           ],
       }

class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = [
            'res_post'
        ]

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.filters['res_post'].queryset = Posts.objects.filter(to_reg_user_id__reg_user_id=self.request)