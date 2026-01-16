from django.db import models
from django.contrib.auth.models import User
import uuid

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

# Create your models here.
class News(BaseModel):
    title = models.CharField(max_length=200)
    image = models.URLField()
    url = models.URLField()
    description = models.TextField()
    content = models.TextField()
    questions_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def generate_questions(self):
        if not self.questions_generated:
            from utils.mcq_generator import generate_mcqs
            from utils.translator import translate_to_hindi

            mcqs = generate_mcqs(self.content, num_questions=5)
            if mcqs:
                ops = ['A', 'B', 'C', 'D']
                for mcq in mcqs:
                    question = Question.objects.create(news=self, question=mcq['question'], question_hi=translate_to_hindi(mcq['question']))

                    for option in ops:
                        Option.objects.create(question=question, option=mcq[option], option_hi=translate_to_hindi(mcq[option]), is_correct= str(mcq['correct']) == option)
                
                print("question created")
            
                News.objects.filter(pk=self.pk).update(questions_generated=True)
                self.questions_generated = True  
                return True
            else:
                print("Failed to generate questions for this news.")
                return False
        else:
            print("Questions already generated for this news.")
            return False

    def save(self, *args, **kwargs):
        should_generate = not self.questions_generated and len(self.content) > 80 
        
        super().save(*args, **kwargs)
        print("should_generate : ", should_generate)
        

        if should_generate:
            import time
            n=20
            for i in range(n):
                print(f"Waiting for {n} seconds {i-n+1}", end='\r', flush=True)
                time.sleep(1)
            print(f"Generating questions for this news [{self.title[:20]}...]")
            self.generate_questions()
        elif not self.content:
            print(f"No content for this news [{self.title[:20]}...]")
    
class Question(BaseModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    
    @property
    def all_options(self):
        return self.options.all()
    
    def __str__(self):
        return f'{self.question}'
    
    class Meta:
        ordering = ['?']

class Option(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.question.question[:40]}-----{self.option[:20]}'
    
    class Meta:
        ordering = ['?']
        
class AttemptQuestion(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    
    def attempts(self, user, question):
        return AttemptQuestion.objects.filter(user=user, question=question).count()

    def __str__(self):
        return f'{self.user.username}--{self.question.question[:40]}--{self.option.option[:20]}'

    class Meta:
        ordering = ['-created_at']
    