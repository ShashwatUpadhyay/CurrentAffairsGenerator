from rest_framework import serializers
from .models import Question,Option, News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['uid','title','image','url','description','content']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['uid','option','is_correct']
        
class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['question','options']