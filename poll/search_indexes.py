import datetime
from haystack import indexes
from poll.models import Question


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    created_by = indexes.EdgeNgramField(model_attr='created_by', null=True, default='')
    created_at = indexes.EdgeNgramField(model_attr='created_at', null=True, default='')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()