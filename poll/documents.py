from django_elasticsearch_dsl import DocType, Index
from .models import Question


questions = Index('questions')
questions.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@questions.doc_type
class QuestionDocument(DocType):
    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'status',
            'created_at'
        ]