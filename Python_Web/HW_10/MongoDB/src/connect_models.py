import pymongo
from datetime import datetime
from mongoengine import connect
from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, DictField

from representers import NoteRepresenter

url = 'mongodb://localhost:27017/hw_10?retryWrites=true&w=majority'

connect(host=url)


class Tag(EmbeddedDocument):
	tag_name = StringField()

	def __hash__(self):
		return hash(self.tag_name)

	def __repr__(self):
		return self.tag_name

	def __str__(self):
		return self.__repr__()


class Note(Document):
	topic = StringField(required=True)
	text = StringField(max_length=200)
	tags = ListField(EmbeddedDocumentField(Tag))
	created_at = DateTimeField(default=datetime.now().isoformat(sep=' ', timespec='seconds'))
	updates = DictField()

	def __repr__(self):
		return NoteRepresenter(self).represent()

	def __str__(self):
		return self.__repr__()

