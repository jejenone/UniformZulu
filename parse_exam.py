from django.core.management import setup_environ
import settings
setup_environ(settings)

import sys, urllib

import re
from BeautifulSoup import ICantBelieveItsBeautifulSoup, MinimalSoup, BeautifulSoup

from django.utils.encoding import smart_unicode

from uniformzulu.models import Question, Module, Answer, Exam

#for fichier in ['reglementation.html', 'mecanique.html', 'preparation.html', 'humain.html', 'communications.html']:
for fichier in ['reglementation_tidy.html']:
	page = open(fichier,'r')

	soup = BeautifulSoup(page,convertEntities=BeautifulSoup.HTML_ENTITIES)

#	print soup.prettify()
	
	for questiontable in soup.findAll('table', width='80%', cellpadding='5'):
		question_num=questiontable.findNext('td',  { "class" : "qcm_examen_no" })
		question_id = int(question_num.contents[0])
		
		try:
			Question.objects.get(pk=question_id)
		except Question.DoesNotExist:
		
			# defaults to PPL(A)
			exam = Exam.objects.get(name='PPLA')
			
			module_name = question_num.contents[2].strip()
			try:
				module = Module.objects.get(name=module_name)
			except Module.DoesNotExist:
				std_num = 24
				if module_name.find('cteurs') > -1:
					std_num = 12
				if module_name.find('nications') > -1:
					std_num = 16
				if module_name.find('paration') > -1:
					std_num = 44
				module = Module(name=module_name, std_num=std_num)
				module.save()
			print "found question "+str(question_id)
	#		print questiontable
			question = Question(pk=question_id, module=Module.objects.get(name=module_name), exam=exam)
	
	
			# recherche annexe
			annexe=False
			question_annexe=questiontable.find('a',  { "class" : "qcm" })
			pic_name = None
			if question_annexe:
				annexe=True
				pic_name = question_annexe['href'].replace('popup.php?photo=','')
				picturefile = 'http://www.chezgligli.net/annexes/ppl/'+ pic_name
				print "retrieving file " + picturefile
				(filename, headers) = urllib.urlretrieve(picturefile, 'media/annexes/'+pic_name)
				question.annexe = pic_name
				print "saved under "+filename
				print
	
			question_text = questiontable.findNext('td',  { "class" : "qcm_examen_question" })
			question_t = ''
			for q in question_text:
	#			print "recherche popup:" + str(q.find('popup.php'))
	#			print q
				if "popup.php" in unicode(q):
					q='<p><a href="'+settings.MEDIA_URL+'annexes/'+pic_name+'" rel="shadowbox">Annexe</a></p>'
					print q
				question_t = question_t + unicode(q).strip() + '\n'
			question.question = question_t
	#		print question.question
		
			# recherche options
			question_options = questiontable.findNext('td',  { "class" : "qcm_examen_options" })
			if question_options.contents:
	#			print type(unicode(question_options.contents))
	#			print "options: " + str(question_options.contents)
				for option in question_options.contents:
	#				question.options = question.options + unicode(option).strip().replace('<br />','') + '\n'
					question.options = question.options + unicode(option).strip()
	#			print "Question " + question_id + ", importing options: " + question.options
	
	
	
	
				
			i=1
			for reponse in questiontable.findAll('td',  { "class" : re.compile("qcm_examen_reponses") }):
				answer_text = ''
				for a_text in reponse:
					answer_text = answer_text + unicode(a_text).strip().replace('<br />','') + '\n'
				answer = None
				try:
					answer = Answer.objects.get(answer=answer_text)
				except Answer.DoesNotExist:
					answer = Answer(answer=answer_text)
					print "saving answer " + str(i) + " for question "+str(question_id)
					answer.save()
					i=i+1
	
				question.answers.add(answer)
				if (answer and str(reponse['class']).find('_bonne') > 0):
					print "correct answer is "+str(answer)
					question.correct_answer = answer
	
			
			print "importing question "+str(question.pk)
			question.save()
