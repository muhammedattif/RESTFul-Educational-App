from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import (
CourseSerializer, CoursesSerializer, UnitSerializer, TopicSerializer, UnitTopicsSerializer, DemoContentSerializer,
FullContentSerializer, QuizSerializer,
QuizResultSerializer, AttachementSerializer,
CommentSerializer, FeedbackSerializer,
QuestionSerializer
)
from courses.models import Course, Unit, Topic, CourseActivity, Content, Comment, Feedback, Quiz, Question, Choice, QuizResult
from playlists.models import WatchHistory
from django.db.models import Q
from functools import reduce
import operator
import courses.utils as utils
import alteby.utils as general_utils
from django.db import IntegrityError
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.db import transaction

from django.db.models import Prefetch

class CourseList(ListAPIView):
    serializer_class = CoursesSerializer

    def get_queryset(self):
        request_params = self.request.GET
        queryset = Course.objects.all()
        if 'q' in request_params:
            search_query = request_params.get('q').split(" ")
            query = reduce(operator.or_, (Q(title__icontains=search_term) | Q(description__icontains=search_term) for search_term in search_query))
            serializer = self.get_serializer()
            return serializer.get_related_queries(queryset.filter(query))
        else:
            serializer = self.get_serializer()
            return serializer.get_related_queries(queryset)

class FeaturedCoursesList(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        serializer = self.get_serializer()
        return serializer.get_related_queries(queryset)



class CourseDetail(APIView):

    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id, prefetch_related=['units', 'categories__course_set', 'privacy__shared_with'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, many=False, context={'request': request})
        return Response(serializer.data)

class ContentDetail(APIView):

    def get(self, request, course_id, content_id, format=None):
        filter_kwargs = {
        'id': content_id,
        'topic__unit__course__id': course_id
        }
        content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs, prefetch_related=['quiz__questions__choices'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            serializer = FullContentSerializer(content, many=False, context={'request': request})
            watch_history, created = WatchHistory.objects.get_or_create(user=request.user)
            watch_history.add_content(content)
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)


class ContentList(APIView, PageNumberPagination):
    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id, prefetch_related=['content__privacy__shared_with'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            contents = course.content.all()
            contents = self.paginate_queryset(contents, request, view=self)
            serializer = DemoContentSerializer(contents, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)


        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

class CourseUnitsList(APIView, PageNumberPagination):
    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if not utils.allowed_to_access_course(request.user, course):
            return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

        units = course.units.all()
        units = self.paginate_queryset(units, request, view=self)
        serializer = UnitSerializer(units, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)



class UnitDetail(APIView):

    def get(self, request, course_id, unit_id, format=None):
        filter_kwargs = {
        'id': unit_id,
        'course__id': course_id
        }
        unit, found, error = utils.get_object(model=Unit, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        serializer = UnitTopicsSerializer(unit, many=False, context={'request': request})
        return Response(serializer.data)

class TopicList(APIView, PageNumberPagination):

    def get(self, request, course_id, unit_id, format=None):
        filter_kwargs = {
        'id': unit_id,
        'course__id': course_id
        }
        unit, found, error = utils.get_object(model=Unit, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        topics = unit.topics.all()
        topics = self.paginate_queryset(topics, request, view=self)
        serializer = TopicSerializer(topics, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

class TopicDetail(APIView, PageNumberPagination):

    def get(self, request, course_id, unit_id, topic_id, format=None):
        filter_kwargs = {
        'id': topic_id,
        'unit__course__id': course_id,
        'unit__id': unit_id
        }
        topic, found, error = utils.get_object(model=Topic, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        content = topic.content.all()
        content = self.paginate_queryset(content, request, view=self)
        serializer = FullContentSerializer(content, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

class QuizDetail(APIView):

    def get(self, request, course_id=None, content_id=None, format=None):

        request_params = self.request.GET
        retake = 0
        if 'retake' in request_params:
            retake = int(request_params.get('retake'))

        if content_id:
            filter_kwargs = {
            'id': content_id,
            'topic__unit__course__id': course_id
            }
            content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs, select_related=['quiz'])
            if not found:
                return Response(error, status=status.HTTP_404_NOT_FOUND)

            if utils.allowed_to_access_content(request.user, content):
                if content.quiz:
                    serializer = QuizSerializer(content.quiz, many=False, context={'request': request})

                    # Delete previous result of this quiz
                    if retake:
                        QuizResult.objects.filter(user=request.user, quiz=content.quiz).delete()

                    return Response(serializer.data)
                else:
                    response = general_utils.error('not_found')
            else:
                response = general_utils.error('access_denied')

            return Response(response, status=status.HTTP_404_NOT_FOUND)

        else:

            course, found, error = utils.get_course(course_id, select_related=['quiz'], prefetch_related=['quiz__questions__choices'])
            if not found:
                return Response(error, status=status.HTTP_404_NOT_FOUND)

            if utils.allowed_to_access_course(request.user, course):
                if course.quiz:
                    serializer = QuizSerializer(course.quiz, many=False, context={'request': request})

                    # Delete previous result of this quiz
                    if retake:
                        QuizResult.objects.filter(user=request.user, quiz=course.quiz).delete()

                    return Response(serializer.data)
                else:
                    response = general_utils.error('not_found')
            else:
                response = general_utils.error('access_denied')

            return Response(response, status=status.HTTP_403_FORBIDDEN)


class CourseQuizAnswer(APIView):

    @transaction.atomic
    def put(self, request, course_id, format=None):

        request_body = request.data
        if 'quiz_answers' not in request_body:
            return Response(general_utils.error('required_fields'), status=status.HTTP_400_BAD_REQUEST)

        quiz_answers = request_body['quiz_answers']

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        quiz = course.quiz
        if not quiz:
            return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)

        answers_objs = []
        for answer in quiz_answers:
            user = request.user
            try:
                question = Question.objects.get(id=answer['question_id'])
                selected_choice = Choice.objects.get(id=answer['selected_choice_id'], question=question)
            except Question.DoesNotExist:
                return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)
            except Choice.DoesNotExist:
                return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)

            answer = QuizResult(user=request.user, quiz=quiz, question=question, selected_choice=selected_choice, is_correct=selected_choice.is_correct)
            answers_objs.append(answer)

        if not answers_objs:
            return Response(general_utils.error('empty_quiz_answers'), status=status.HTTP_400_BAD_REQUEST)

        QuizResult.objects.bulk_create(answers_objs)
        return Response(general_utils.success('quiz_answer_submitted'), status=status.HTTP_201_CREATED)

class ContentQuizAnswer(APIView):

    @transaction.atomic
    def put(self, request, course_id, content_id, format=None):

        request_body = request.data
        if 'quiz_answers' not in request_body:
            return Response(general_utils.error('required_fields'), status=status.HTTP_400_BAD_REQUEST)

        quiz_answers = request_body['quiz_answers']

        filter_kwargs = {
        'id': content_id,
        'topic__unit__course__id': course_id
        }
        content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs, select_related=['quiz'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        quiz = content.quiz
        if not quiz:
            return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)

        answers_objs = []
        for answer in quiz_answers:
            user = request.user
            try:
                question = Question.objects.get(id=answer['question_id'])
                selected_choice = Choice.objects.get(id=answer['selected_choice_id'], question=question)
            except Question.DoesNotExist:
                return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)
            except Choice.DoesNotExist:
                return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)

            answer = QuizResult(user=request.user, quiz=quiz, question=question, selected_choice=selected_choice, is_correct=selected_choice.is_correct)
            answers_objs.append(answer)

        if not answers_objs:
            return Response(general_utils.error('empty_quiz_answers'), status=status.HTTP_400_BAD_REQUEST)

        QuizResult.objects.bulk_create(answers_objs)
        return Response(general_utils.success('quiz_answer_submitted'), status=status.HTTP_201_CREATED)

class CourseQuizResult(APIView):

    def get(self, request, course_id):

        course, found, error = utils.get_course(course_id, prefetch_related=['quiz__questions'], select_related=['quiz'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        quiz = course.quiz
        if not quiz:
            return Response(general_utils.error('not_found'), status=status.HTTP_404_NOT_FOUND)

        serializer = QuizResultSerializer(course.quiz, many=False, context={'request': request})
        return Response(serializer.data)


class ContentQuizResult(APIView):

    def get(self, request, course_id, content_id):
        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        filter_kwargs = {
        'id': content_id,
        'topic__unit__course__id': course_id
        }
        content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        quiz = content.quiz
        quiz_answers = QuizResult.objects.filter(user=request.user, quiz=quiz)
        serializer = QuizResultSerializer(quiz_answers, many=True, context={'request': request})
        return Response(serializer.data)

class CourseAttachement(APIView):

    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            attachments = course.attachments.all()

            serializer = AttachementSerializer(attachments, many=True, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

class ContentAttachement(APIView):

    def get(self, request, course_id, content_id, format=None):

        filter_kwargs = {
        'id': content_id,
        'topic__unit__course__id': course_id
        }
        content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            attachments = content.attachments.all()
            serializer = AttachementSerializer(attachments, many=True, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

class CourseComments(APIView):
    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            comments = course.comments(manager='course_comments').all()
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)


    def post(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            comment_body = request.data['comment_body']
            comment = Comment.objects.create(user=request.user, course=course, comment_body=comment_body)
            serializer = CommentSerializer(comment, many=False, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)


class ContentComments(APIView):
    def get(self, request, course_id, content_id, format=None):

        filter_kwargs = {
        'id': content_id,
        'topic__unit__course__id': course_id
        }
        content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs, prefetch_related=['comments', 'privacy'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            comments = content.comments(manager='content_comments').all()
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)

    def post(self, request, course_id, content_id, format=None):
        filter_kwargs = {
        'id': content_id,
        'topic__unit__course__id': course_id
        }
        content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            comment_body = request.data['comment_body']
            comment = Comment.objects.create(user=request.user, course=content.course, content=content, comment_body=comment_body)
            serializer = CommentSerializer(comment, many=False, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)



class CourseFeedbacks(APIView, PageNumberPagination):

    def get(self, request, course_id, format=None):
        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        feedbacks = course.feedbacks.all()
        feedbacks = self.paginate_queryset(feedbacks, request, view=self)
        serializer = FeedbackSerializer(feedbacks, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


    def post(self, request, course_id, format=None):
        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.is_enrolled(request.user, course):
            rating = request.data['rating']
            description = request.data['description']
            try:
                feedback = Feedback.objects.create(user=request.user, course=course, rating=rating, description=description)
            except IntegrityError as e:
                response = {
                    'status': 'error',
                    'message': str(e),
                    'error_description': 'Ensure that rating value is less than or equal to 5 and more than or equal to 1.'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            serializer = FeedbackSerializer(feedback, many=False, context={'request': request})
            return Response(serializer.data)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)


class TrackCourseActivity(APIView):

    def post(self, request, course_id, content_id, format=None):
        filter_kwargs = {
        'id': content_id,
        'topic__unit__course__id': course_id
        }
        content, found, error = utils.get_object(model=Content, filter_kwargs=filter_kwargs)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.is_enrolled(request.user, content.course):
            CourseActivity.objects.get_or_create(user=request.user, course=content.course, content=content)
            response = {
                'status': 'success',
                'message': 'Checked!',
                'success_description': 'This content Marked ad read.'
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        return Response(general_utils.error('access_denied'), status=status.HTTP_403_FORBIDDEN)
