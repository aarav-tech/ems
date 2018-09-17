import datetime
from haystack import indexes
from poll.models import Question


class QuestionIndex(indexes.ModelSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.IntegerField(model_attr='id')
    created_by = indexes.IntegerField(model_attr='created_by__id', null=True, default=0)

    class Meta:
        model = Question
        fields = ["text", "id", "title", "created_by", "created_at"]

    # def index_queryset(self, using=None):
    #     """Used when the entire index for model is updated."""
    #     return self.get_model().objects.all()