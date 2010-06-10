from django.core.management import setup_environ
import settings
setup_environ(settings)

import sys, urllib

import re

from django.utils.encoding import smart_unicode

from uniformzulu.models import Question, Module, Answer, Exam

#for fichier in ['reglementation.html', 'mecanique.html', 'preparation.html', 'humain.html', 'communications.html']:

default_exam = Exam.objects.get(name='PPLA')

for question in Question.objects.select_related().all():

	if not question.exam:
		print "question "+question.pk+" has not exam type, setting to "+str(default_exam)
		question.exam = default_exam
		question.save()
				
	answer_count = question.answers.count()
	if answer_count > 4:
		print "Question "+str(question.pk)+" has more than 4 answers ("+str(answer_count)+")"
		answers = question.answers.all()
		print "correct is: "+str(question.correct_answer.pk)
		for j,i in enumerate([7,5,6,4]):
			try:
				answer = answers[i]
				answer.delete()
			except IndexError:
				continue