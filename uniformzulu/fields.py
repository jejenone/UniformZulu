from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django import forms
from django.forms.widgets import RadioFieldRenderer, RadioInput, RadioSelect
from django.utils.encoding import StrAndUnicode, force_unicode
from django.db import models
import uuid

class ReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
            return mark_safe("<p %s>%s</p>" % (flatatt(final_attrs), escape(value) or ''))

    def _has_changed(self, initial, data):
        return False

class ReadOnlyField(forms.Field):
    widget = ReadOnlyWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        super(type(self), self).__init__(self, label=label, initial=initial, 
            help_text=help_text, widget=widget)
        self.widget.initial = initial

    def clean(self, value):
        return self.widget.initial


class MyRadioRenderer(RadioFieldRenderer):
	def render(self):
		return mark_safe(u'\n'.join([u'%s<br>'
			% force_unicode(w) for w in self]))       
 
	def __iter__(self):
		for i, choice in enumerate(self.choices):
			yield RadioInput(self.name, self.value, self.attrs.copy(), choice, i)

 
# class UUIDField(models.CharField):
#     """
#         A field which stores a UUID value in hex format. This may also have
#         the Boolean attribute 'auto' which will set the value on initial save to a
#         new UUID value (calculated using the UUID1 method). Note that while all
#         UUIDs are expected to be unique we enforce this with a DB constraint.
#     """
#     __metaclass__ = models.SubfieldBase
#  
#     def __init__(self, version=4, node=None, clock_seq=None, namespace=None, auto=False, name=None, *args, **kwargs):
#         assert(version in (1, 3, 4, 5), "UUID version %s is not supported." % (version,))
#         self.auto = auto
#         self.version = version
#         # Set this as a fixed value, we store UUIDs in text.
#         kwargs['max_length'] = 32
#         if auto:
#             # Do not let the user edit UUIDs if they are auto-assigned.
#             kwargs['editable'] = False
#             kwargs['blank'] = True
#             kwargs['unique'] = True
#         if version == 1:
#             self.node, self.clock_seq = node, clock_seq
#         elif version in (3, 5):
#             self.namespace, self.name = namespace, name
#         super(UUIDField, self).__init__(*args, **kwargs)
#  
#     def _create_uuid(self):
#         if self.version == 1:
#             args = (self.node, self.clock_seq)
#         elif self.version in (3, 5):
#             args = (self.namespace, self.name)
#         else:
#             args = ()
#         return getattr(uuid, 'uuid%s' % (self.version,))(*args)
#  
#     def db_type(self):
#         return 'char'
#  
#     def pre_save(self, model_instance, add):
#         """ see CharField.pre_save
#             This is used to ensure that we auto-set values if required.
#         """
#         value = getattr(model_instance, self.attname, None)
#         if not value and self.auto:
#             # Assign a new value for this attribute if required.
#             value = self._create_uuid()
#             setattr(model_instance, self.attname, value)
#         return value
#  
#     def to_python(self, value):
#         if not value: return
#         if not isinstance(value, uuid.UUID):
#             value = uuid.UUID(value)
#         return value
#  
#     def get_db_prep_save(self, value):
#         if not value: return
#         assert(isinstance(value, uuid.UUID))
#         return value.hex
#  
#     def get_db_prep_value(self, value):
# 		if not value: return
# 		if not isinstance(value, uuid.UUID):
# 			value = uuid.UUID(value)
# 		return value.hex #unicode(value)
# #        assert(isinstance(value, uuid.UUID))
# #        return unicode(value)