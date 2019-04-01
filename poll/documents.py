from django_elasticsearch_dsl import DocType, Index, fields
from .models import Question

question = Index('questions')
question.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@question.doc_type
class QuestionDocument(DocType):

    class Meta:
        model = Question
        fields = [
            'title',
            'status',
            # 'created_by',
            'start_date',
            'end_date'
        ]