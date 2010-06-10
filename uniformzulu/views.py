from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from django.forms.formsets import formset_factory
from models import Module, Question, Answer
from models import Quizz2, QuizzQuestion, Exam
import random
import fields
from django.core import serializers
from django.utils import simplejson
from django.http import HttpResponseRedirect, QueryDict
import datetime
from django.db.models import F
from django.core.urlresolvers import reverse
import settings

# http://dmitko.ru/?p=546
from uniformzulu.forms import ReCaptchaRegistrationForm
#import profile
def user_created(sender, user, request, **kwargs):
	form = ReCaptchaRegistrationForm(request.POST)
	user.first_name = form.data["first_name"]
	user.last_name = form.data["last_name"]
	user.save()

from registration.signals import user_registered
user_registered.connect(user_created)

def xd_receiver(request):
    return render_to_response('uniformzulu/xd_receiver.htm')

def login_form(request):
	from django.contrib.auth.forms import AuthenticationForm
	login_form = AuthenticationForm()
	next = request.path
	return {'login_form': login_form, 'next': next}

def main(request):
	modules = Module.objects.all()
	
	quizzes = None
#	quizzes = Quizz2.objects.filter(user=request.user).filter(submitted__isnull=False)

	# stats for graphs
	module_pie_labels = list()
	module_pie_data = list()
	module_stats = list()
	
	if request.user.is_authenticated():
		quizzes = Quizz2.objects.filter(user=request.user).filter(submitted__isnull=False)
		module_pie_data = [quizzes.filter(module=module).count() for module in modules]
		for i,module in enumerate(modules):
			if module_pie_data[i]:
				module_pie_labels.append(module.name+' ('+str(module_pie_data[i])+')')
				quiz_by_module = quizzes.filter(module=module).order_by('submitted').reverse()[:10]
				module_stats.append((module,quiz_by_module,[quiz.get_score_int_pct() for quiz in reversed(quiz_by_module)]))
	#	raise Exception( quiz_by_module)
	# end stats
	
	
	return render_to_response('uniformzulu/index.html', {'modules':modules, 'quizzes': quizzes, 'module_pie_data': module_pie_data, 'module_pie_labels': module_pie_labels, 'module_stats': module_stats}, context_instance=RequestContext(request))

class QuestionForm(forms.Form):
	answers = forms.ChoiceField(widget=forms.RadioSelect(renderer=fields.MyRadioRenderer, attrs={'class':'toto'}),label=None, required=True)
    
	def __init__(self, *args, **kwargs):
		question = kwargs.pop("question")
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.problem = question.question
		if question.options:
			self.options = question.options
		if question.annexe:
			self.annexe = question.annexe
		answers = question.answers.order_by('answer')
		self.fields['answers'].choices = [(i, a.answer) for i, a in enumerate(answers)]
		
		# We need to work out the position of the correct answer in the
		# sorted list of all possible answers.
		for pos, answer in enumerate(answers):
			if answer.id == question.correct_answer_id:
				self.correct = pos
				break
	
#	def clean_answers(self):
#		data = self.cleaned_data['answers']
#		print "clean data: "+data
#		return data
		
	def is_correct(self):
		"""
		Determines if the given answer is correct (for a bound form).
		"""
		if not self.is_valid():
		    return False
		if not self.cleaned_data:
			return False
		return self.cleaned_data['answers'] == str(self.correct)


	def answers_fields(self):
		field = self['answers']
		return field.as_widget(field.field.widget)

class QuizzQuestionForm(forms.Form):
	answers = forms.ChoiceField(widget=forms.RadioSelect(renderer=fields.MyRadioRenderer, attrs={}),label=None, required=True)
    
	def __init__(self, *args, **kwargs):
		question = kwargs.pop("question")
		super(QuizzQuestionForm, self).__init__(*args, **kwargs)
		self.question = question.question
		self.problem = question.question.question
		if question.question.options:
			self.options = question.question.options
		if question.question.annexe:
			self.annexe = question.question.annexe
		answers = question.question.answers.all()
		self.fields['answers'].choices = [(i, a.answer) for i, a in enumerate(answers)]

		# We need to work out the position of the correct answer in the
		# sorted list of all possible answers.
		for pos, answer in enumerate(answers):
			if answer.id == question.question.correct_answer_id:
				self.correct = pos
				break
				
		# jeje - initial value if given_answer
		if question.given_answer:
			for pos, answer in enumerate(answers):
				if question.given_answer == answer:
					self.fields['answers'].initial = pos

	def get_cleaned_or_initial(self, fieldname):
		if hasattr(self, 'cleaned_data'):
			return self.cleaned_data.get(fieldname)
		else:
			return str(self[fieldname].field.initial)

	def is_correct(self):
		return self.get_cleaned_or_initial('answers') == str(self.correct)

	def answers_fields(self):
		field = self['answers']
		return field.as_widget(field.field.widget)



class CustomBaseFormset(forms.formsets.BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.questions = list(kwargs.pop("questions"))
        self.extra = len(self.questions)
        super(CustomBaseFormset, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs["question"] = self.questions[i]
        return super(CustomBaseFormset, self)._construct_form(i, **kwargs)

		
@login_required
def quiz_form(request,uuid):

	quiz = get_object_or_404(Quizz2.objects.select_related().all(), pk=uuid)
	
	if quiz.submitted or request.method=='POST':

		formset = None

		# nouveau quizz non repondu
		if request.method=='POST' and not quiz.submitted:
			formset = create_quiz_formset(quiz, request.POST)
			if formset.is_valid():
				for i,fields in enumerate([f.cleaned_data for f in formset.forms]):
					if 'answers' in fields:
						qq = quiz.quizzquestion_set.select_related().get(position=i)
						qq.given_answer = qq.question.answers.all()[int(fields['answers'])]
						qq.save()
				quiz.submitted = datetime.datetime.now()
				quiz.save()
					
		# quizz deja effectue
		else:
			formset = create_quiz_formset(quiz)
		
		
		if 'django.contrib.comments' in settings.INSTALLED_APPS:
			return render_to_response('uniformzulu/correction_comments.html',{'quiz':quiz, 'formset': formset}, context_instance=RequestContext(request))
		else:
			return render_to_response('uniformzulu/correction.html',{'quiz':quiz, 'formset': formset}, context_instance=RequestContext(request))		

	else:
		formset = create_quiz_formset(quiz)
		return render_to_response('uniformzulu/quiz.html',{'formset': formset, 'quiz':quiz}, context_instance=RequestContext(request))


@login_required
def get_quiz(request,module_id):
	module = get_object_or_404(Module,pk=module_id)
	quiz = Quizz2.objects.filter(user=request.user).filter(module=module).filter(submitted__isnull=True)
	if quiz and ('new' in request.GET):
		quiz.delete()
		quiz = None
	if not quiz:
		quiz = create_quiz(request.user,module)
	else:
		quiz = quiz[0]
	return HttpResponseRedirect(reverse('quiz_form', args=[str(quiz.uuid)]))

@login_required
def get_quiz_hard(request,module_id):
	module = get_object_or_404(Module,pk=module_id)
#	quiz = Quizz2.objects.filter(user=request.user).filter(module=module).filter(submitted__isnull=True)
#	if quiz and ('new' in request.GET):
#		quiz.delete()
#		quiz = None
#	if not quiz:
	qqset = create_quiz_hard(request.user,module)
#	else:
#		quiz = quiz[0]
	return render_to_response('uniformzulu/quiz_hard.html',{'qqset':qqset}, context_instance=RequestContext(request))
#	return HttpResponseRedirect('/uz/quiz_hard/'+str(quiz.uuid))


def create_quiz_formset(quiz,data=None):
	quizzquestions = quiz.quizzquestion_set.select_related().all()
	QuizFormset = forms.formsets.formset_factory(QuizzQuestionForm, CustomBaseFormset)
	formset = QuizFormset(data, questions=quizzquestions)
	return formset

def create_quiz(user,module):
	questions = list()
	questions = random.sample(Question.objects.filter(exam__name='PPLA',module=module),module.std_num)
	quiz = Quizz2(user=user,module=module)
	quiz.save()
	count = 0
	for q in questions:
		qq = QuizzQuestion(quizz=quiz,question=q,position=count)
		qq.save()
		count +=1
	return quiz

def create_quiz_hard(user,module):
	questions = list()
	qqset = QuizzQuestion.objects.filter(quizz__user=user, question__module=module).exclude(given_answer=F('question__correct_answer')).order_by('question__id')
	qset = Question.objects.filter(question__in=qqset__question)
#	qqset = Question.objects.get_qqset_for_user(user)
#	qqset = Question.objects.filter(module=module, correct_answer=F('quizzquestion__given_answer')).order_by('id')
	quiz = Quizz2(user=user, module=module)
#	quiz.save()
#	count = 0
#	for q in qqset:
#		qq = QuizzQuestion(quizz=quiz,question=q.question,position=count)
#		count +=1
#		qq.save()
	return qqset
	