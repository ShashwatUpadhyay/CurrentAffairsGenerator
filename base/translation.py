from modeltranslation.translator import register, TranslationOptions
from .models import Question, Option, News

@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question',)

@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('option',)

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'content')