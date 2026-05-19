from django.forms import ModelForm

from posts.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "rate", "category", "image"]


# class TestForm(Form):
#     title = CharField(max_length=255, required=False)
#     content = CharField(required=False)
#     rate = IntegerField(min_value=1, max_value=10, required=False)
#     category = IntegerField(required=False)
#     image = ImageField(required=False)
#     tags = CharField(required=False)

#     def clean_title(self):
#         test_title = self.cleaned_data["title"]

#         if test_title == "Запрещенное слово!":
#             raise ValidationError("Вы ввели запрещенное слово!")

#         test_title = f"{test_title}    Пост"

#         return test_title
