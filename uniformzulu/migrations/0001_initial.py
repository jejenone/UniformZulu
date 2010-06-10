
from south.db import db
from django.db import models
from UniformZulu.uniformzulu.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Question'
        db.create_table('uniformzulu_question', (
            ('id', orm['uniformzulu.Question:id']),
            ('module', orm['uniformzulu.Question:module']),
            ('exam', orm['uniformzulu.Question:exam']),
            ('question', orm['uniformzulu.Question:question']),
            ('options', orm['uniformzulu.Question:options']),
            ('annexe', orm['uniformzulu.Question:annexe']),
            ('correct_answer', orm['uniformzulu.Question:correct_answer']),
        ))
        db.send_create_signal('uniformzulu', ['Question'])
        
        # Adding model 'Exam'
        db.create_table('uniformzulu_exam', (
            ('name', orm['uniformzulu.Exam:name']),
        ))
        db.send_create_signal('uniformzulu', ['Exam'])
        
        # Adding model 'Quizz2'
        db.create_table('uniformzulu_quizz2', (
            ('uuid', orm['uniformzulu.Quizz2:uuid']),
            ('user', orm['uniformzulu.Quizz2:user']),
            ('module', orm['uniformzulu.Quizz2:module']),
            ('created', orm['uniformzulu.Quizz2:created']),
            ('submitted', orm['uniformzulu.Quizz2:submitted']),
        ))
        db.send_create_signal('uniformzulu', ['Quizz2'])
        
        # Adding model 'Module'
        db.create_table('uniformzulu_module', (
            ('id', orm['uniformzulu.Module:id']),
            ('name', orm['uniformzulu.Module:name']),
            ('std_num', orm['uniformzulu.Module:std_num']),
        ))
        db.send_create_signal('uniformzulu', ['Module'])
        
        # Adding model 'Answer'
        db.create_table('uniformzulu_answer', (
            ('id', orm['uniformzulu.Answer:id']),
            ('answer', orm['uniformzulu.Answer:answer']),
        ))
        db.send_create_signal('uniformzulu', ['Answer'])
        
        # Adding model 'QuizzQuestion'
        db.create_table('uniformzulu_quizzquestion', (
            ('id', orm['uniformzulu.QuizzQuestion:id']),
            ('quizz', orm['uniformzulu.QuizzQuestion:quizz']),
            ('question', orm['uniformzulu.QuizzQuestion:question']),
            ('position', orm['uniformzulu.QuizzQuestion:position']),
            ('given_answer', orm['uniformzulu.QuizzQuestion:given_answer']),
        ))
        db.send_create_signal('uniformzulu', ['QuizzQuestion'])
        
        # Adding ManyToManyField 'Question.answers'
        db.create_table('uniformzulu_question_answers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm.Question, null=False)),
            ('answer', models.ForeignKey(orm.Answer, null=False))
        ))
        
        # Creating unique_together for [module, id] on Question.
        db.create_unique('uniformzulu_question', ['module_id', 'id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [module, id] on Question.
        db.delete_unique('uniformzulu_question', ['module_id', 'id'])
        
        # Deleting model 'Question'
        db.delete_table('uniformzulu_question')
        
        # Deleting model 'Exam'
        db.delete_table('uniformzulu_exam')
        
        # Deleting model 'Quizz2'
        db.delete_table('uniformzulu_quizz2')
        
        # Deleting model 'Module'
        db.delete_table('uniformzulu_module')
        
        # Deleting model 'Answer'
        db.delete_table('uniformzulu_answer')
        
        # Deleting model 'QuizzQuestion'
        db.delete_table('uniformzulu_quizzquestion')
        
        # Dropping ManyToManyField 'Question.answers'
        db.delete_table('uniformzulu_question_answers')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'uniformzulu.answer': {
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'uniformzulu.exam': {
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'})
        },
        'uniformzulu.module': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'std_num': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'uniformzulu.question': {
            'Meta': {'unique_together': "(('module', 'id'),)"},
            'annexe': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['uniformzulu.Answer']"}),
            'correct_answer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'correct_answer'", 'to': "orm['uniformzulu.Answer']"}),
            'exam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniformzulu.Exam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniformzulu.Module']"}),
            'options': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'uniformzulu.quizz2': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniformzulu.Module']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'uuid': ('UUIDField', [], {'auto': 'True', 'primary_key': 'True'})
        },
        'uniformzulu.quizzquestion': {
            'given_answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniformzulu.Answer']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniformzulu.Question']"}),
            'quizz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniformzulu.Quizz2']"})
        }
    }
    
    complete_apps = ['uniformzulu']
