from django.contrib import admin

from uniformzulu.models import Question, Module, Answer
from uniformzulu.models import QuizzQuestion, Quizz2, Exam

class ModuleAdmin(admin.ModelAdmin):
	list_display = ('name',)

class ExamAdmin(admin.ModelAdmin):
	list_display = ('name',)

class QuestionAdmin(admin.ModelAdmin):
	list_display = ('id', 'module', 'question',)
	list_filter = ('module',)
	search_fields = ['question']

class AnswerAdmin(admin.ModelAdmin):
	list_display = ('answer',)

class Quizz2Admin(admin.ModelAdmin):
	list_display = ('uuid', 'user', 'module', 'created', 'submitted', 'get_score_str_absolute', 'get_score_str_pct')
	list_filter = ('user', 'module', 'created')

class QuizzQuestionAdmin(admin.ModelAdmin):
	list_display = ('quizz', 'question', 'given_answer')
	
admin.site.register(Module, ModuleAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Quizz2, Quizz2Admin)
admin.site.register(QuizzQuestion, QuizzQuestionAdmin)

