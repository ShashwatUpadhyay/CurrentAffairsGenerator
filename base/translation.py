from modeltranslation.translator import register, TranslationOptions
from .models import Question, Option

@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('question',)

@register(Option)
class OptionTranslationOptions(TranslationOptions):
    fields = ('option',)
