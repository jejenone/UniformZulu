from django.db import models
from django.contrib.auth.models import User
#from fields import UUIDField
from django_extensions.db.fields import UUIDField
from django.db.models import F

class Module(models.Model):
	name = models.CharField(max_length=40)
	std_num = models.PositiveIntegerField("Default number of questions")
	
	def __unicode__(self):
		return self.name


class Answer(models.Model):
	answer = models.CharField(max_length=1000)

	def __unicode__(self):
		return self.answer

EXAM_CHOICES = (
	('PPLA', 'PPL/A'),
	('PPLH', 'PPL/H'),
	('ATPL', 'ATPL'),
	)
class Exam(models.Model):
	name = models.CharField(choices=EXAM_CHOICES, max_length=4, primary_key=True)

	def __unicode__(self):
		return str(self.name)

class QuestionManager(models.Manager):
	def get_qqset_for_user(self, user):
		qqset = self.quizzquestion_set.filter(quizz__user=user)
		return qqset

class Question(models.Model):

	objects = QuestionManager()
	
	module = models.ForeignKey(Module)
	exam = models.ForeignKey(Exam)
	question = models.TextField()
	options = models.TextField(blank=True)
	annexe = models.TextField(blank=True)
	answers = models.ManyToManyField(Answer)
	correct_answer = models.ForeignKey(Answer, related_name="correct_answer")
	
	def __unicode__(self):
		return self.question
	
	class Meta:
		unique_together = (("module","id"))

	def get_answered_count(self, user=None):
		qq = self.quizzquestion_set.filter(quizz__submitted__isnull=False)
		if user:
			count = qq.filter(quizz__user=user).count()
		else:
			count = qq.count()
		return count

class Quizz2(models.Model):
	uuid = UUIDField(primary_key=True, auto=True)
	user = models.ForeignKey(User)
	module = models.ForeignKey(Module)
	created = models.DateTimeField(auto_now_add=True)
	submitted = models.DateTimeField(null=True)
	
	def __unicode__(self):
		return self.uuid
			
# 	def get_score(self, qq_set):
# 		score = 0
# 		for qq in qq_set:
# 			if qq.is_good():
# 				score += 1
# 		return score
	
	def get_score_str_absolute(self):
		if self.submitted:
			# use select_related for much better performances to retrieve the related question objects
			qq_set = self.quizzquestion_set
			# F() object is much more powerful!
			good_count = qq_set.filter(given_answer=F('question__correct_answer')).count()
			return str(good_count)+'/'+str(qq_set.count())
#			return str(self.get_score(qq_set))+'/'+str(qq_set.count())
		else:
			return None
	
	def get_score_int_pct(self):
		if self.submitted:
			# use select_related for much better performances to retrieve the related question objects
			qq_set = self.quizzquestion_set
			# F() object is much more powerful!
			good_count = qq_set.filter(given_answer=F('question__correct_answer')).count()
			return(int(good_count*100/qq_set.count()))
#			return(int(self.get_score(qq_set)*100/qq_set.count()))
		else:
			return None
		
	def get_score_str_pct(self):
		if self.submitted:
			return str(self.get_score_int_pct())+'%'
		else:
			return None


class QuizzQuestion(models.Model):
	quizz = models.ForeignKey(Quizz2)
	question = models.ForeignKey(Question)
	position = models.PositiveIntegerField()
	given_answer = models.ForeignKey(Answer, null=True)
	
	def __unicode__(self):
		return str(self.position) + ' q_id: ' + str(self.question.id) + ' - ' + str(self.quizz)
	
	def is_good(self):
		return self.given_answer == self.question.correct_answer

	class Meta:
		ordering = ('position',)
