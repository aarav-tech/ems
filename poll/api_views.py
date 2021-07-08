from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.decorators import action

from poll.forms import PollForm, ChoiceForm
from poll.models import *
from poll.serializers import (
    QuestionSerializer,
    ChoiceSerializer,
    QuestionSearchSerializer,
)


class QuestionSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionSearchSerializer

    def get_queryset(self):
        result = QuestionDocument.search()


class PollFilter(FilterSet):
    tags = filters.CharFilter(method="filter_by_tags")

    class Meta:
        model = Question
        fields = ["tags"]

    def filter_by_tags(self, queryset, name, value):
        tag_names = value.strip().split(",")
        tags = Tag.objects.filter(name__in=tag_names)
        return queryset.filter(tags__in=tags).distinct()


class PollViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = "id"
    filter_backends = (DjangoFilterBackend,)
    filter_class = PollFilter
    authentication_classes = (TokenAuthentication,)

    @action(detail=True, methods=["GET"])
    def choices(self, request, id=None):
        question = self.get_object()
        choices = Choice.objects.filter(question=question)
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["POST"])
    def choice(self, request, id=None):
        question = self.get_object()
        data = request.data
        data["question"] = question.id
        serializer = ChoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)

class PollListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    lookup_field = "id"
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication,
        BasicAuthentication,
    ]
    permission_classes = [IsAuthenticated, IsAdminUser]


    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def put(self, request, id=None):
        return self.update(request, id)

    def perform_update(self, serializer):
        print(self.request.user)
        serializer.save(created_by=self.request.user)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class PollAPIView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serailizer = QuestionSerializer(questions, many=True)
        return Response(serailizer.data, status=200)

    def post(self, request):
        data = request.data
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.erros, status=400)


class PollDetailView(APIView):
    def get_object(self, id):
        try:
            return Question.objects.get(id=id)
        except Question.DoesNotExist as e:
            return Response({"error": "Given question object not found."}, status=404)

    def get(self, request, id=None):
        instance = self.get_object(id)
        serailizer = QuestionSerializer(instance)
        return Response(serailizer.data)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = QuestionSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.erros, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)


@csrf_exempt
def poll(request):
    if request.method == "GET":
        questions = Question.objects.all()
        serailizer = QuestionSerializer(questions, many=True)
        return JsonResponse(serailizer.data, safe=False)

    elif request.method == "POST":
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def poll_details(request, id):
    try:
        instance = Question.objects.get(id=id)
    except Question.DoesNotExist as e:
        return JsonResponse({"error": "Given question object not found."}, status=404)

    if request.method == "GET":
        serailizer = QuestionSerializer(instance)
        return JsonResponse(serailizer.data)

    elif request.method == "PUT":
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = QuestionSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.erros, status=400)

    elif request.method == "DELETE":
        instance.delete()
        return HttpResponse(status=204)
