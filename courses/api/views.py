from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CourseSerializer, DemoContentSerializer, FullContentSerializer, QuizSerializer, AttachementSerializer, CommentSerializer, FeedbackSerializer
from courses.models import Course, CourseProgress, Content, Comment, Feedback, Quiz
from playlists.models import WatchHistory
from django.db.models import Q
from functools import reduce
import operator
import courses.utils as utils
from django.db import IntegrityError

class CourseList(APIView, PageNumberPagination):
    def get(self, request, format=None):


        request_params = request.GET
        if request_params:
            search_query = request_params.get('q').split(" ")
            query = reduce(operator.or_, (Q(title__icontains=search_term) | Q(description__icontains=search_term) for search_term in search_query))
            courses = Course.objects\
                .prefetch_related('content__quiz__questions__choices', 'content__privacy', 'categories', 'privacy__shared_with')\
                .filter(query)
        else:
            courses = Course.objects.prefetch_related('content__quiz__questions__choices', 'content__privacy', 'categories', 'privacy__shared_with')

        courses = self.paginate_queryset(courses, request, view=self)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseDetail(APIView, PageNumberPagination):

    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id, prefetch_related=['privacy__shared_with'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            serializer = CourseSerializer(course, many=False)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

class ContentDetail(APIView):

    def get(self, request, course_id, content_id, format=None):
        content, found, error = utils.get_content(content_id, course_id=course_id, prefetch_related=['quiz__questions__choices'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            serializer = FullContentSerializer(content, many=False)
            watch_history, created = WatchHistory.objects.get_or_create(user=request.user)
            watch_history.add_content(content)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

class ContentList(APIView, PageNumberPagination):
    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            contents = Content.objects.prefetch_related('privacy__shared_with').filter(course__id=course_id)
            contents = self.paginate_queryset(contents, request, view=self)
            serializer = DemoContentSerializer(contents, many=True, context={'request': request})
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

class QuizDetail(APIView, PageNumberPagination):

    def get(self, request, course_id=None, content_id=None, format=None):
        if content_id:
            content, found, error = utils.get_content(content_id, course_id=course_id, select_related=['quiz'])
            if not found:
                return Response(error, status=status.HTTP_404_NOT_FOUND)

            if utils.allowed_to_access_content(request.user, content):
                if content.quiz:
                    quiz_id = content.quiz.id
                    quiz = Quiz.objects.prefetch_related('questions__choices').get(id=quiz_id)
                    serializer = QuizSerializer(quiz, many=False)
                    return Response(serializer.data)
                else:
                    response = {
                        'status': 'error',
                        'message': 'Not Found!',
                        'error_description': 'This content does not has any quizzes.'
                    }
            else:
                response = utils.errors['access_denied']

            return Response(response, status=status.HTTP_404_NOT_FOUND)

        else:

            course, found, error = utils.get_course(course_id, select_related=['quiz'])
            if not found:
                return Response(error, status=status.HTTP_404_NOT_FOUND)

            if utils.allowed_to_access_course(request.user, course):
                if course.quiz:
                    quiz_id = course.quiz.id
                    quiz = Quiz.objects.prefetch_related('questions__choices').get(id=quiz_id)
                    serializer = QuizSerializer(quiz, many=False)
                    return Response(serializer.data)
                else:
                    response = {
                        'status': 'error',
                        'message': 'Not Found!',
                        'error_description': 'This course does not has any quizzes.'
                    }
            else:
                response = utils.errors['access_denied']

            return Response(response, status=status.HTTP_403_FORBIDDEN)


class CourseAttachement(APIView):

    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            attachments = course.attachments.all()
            serializer = AttachementSerializer(attachments, many=True)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

class ContentAttachement(APIView):

    def get(self, request, course_id, content_id, format=None):

        content, found, error = utils.get_content(content_id, course_id=course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            attachments = content.attachments.all()
            serializer = AttachementSerializer(attachments, many=True)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

class CourseComments(APIView):
    def get(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            comments = course.comments(manager='course_comments').all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)


    def post(self, request, course_id, format=None):

        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_course(request.user, course):
            comment_body = request.data['comment_body']
            comment = Comment.objects.create(user=request.user, course=course, comment_body=comment_body)
            serializer = CommentSerializer(comment, many=False)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)


class ContentComments(APIView):
    def get(self, request, course_id, content_id, format=None):

        content, found, error = utils.get_content(content_id, course_id=course_id, prefetch_related=['comments', 'privacy'])
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            comments = content.comments(manager='content_comments').all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)

    def post(self, request, course_id, content_id, format=None):
        content, found, error = utils.get_content(content_id, course_id=course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.allowed_to_access_content(request.user, content):
            comment_body = request.data['comment_body']
            comment = Comment.objects.create(user=request.user, course=content.course, content=content, comment_body=comment_body)
            serializer = CommentSerializer(comment, many=False)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)



class CourseFeedbacks(APIView, PageNumberPagination):

    def get(self, request, course_id, format=None):
        course, found, error = utils.get_course(course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        feedbacks = course.feedbacks.all()
        feedbacks = self.paginate_queryset(feedbacks, request, view=self)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)


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

            serializer = FeedbackSerializer(feedback, many=False)
            return Response(serializer.data)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)


class UpdateCourseProgress(APIView):

    def get(self, request, course_id, content_id, format=None):
        content, found, error = utils.get_content(content_id, course_id=course_id)
        if not found:
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        if utils.is_enrolled(request.user, content.course):
            CourseProgress.objects.get_or_create(user=request.user, course=content.course, content=content)
            response = {
                'status': 'success',
                'message': 'Checked!',
                'success_description': 'This content Marked ad read.'
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        return Response(utils.errors['access_denied'], status=status.HTTP_403_FORBIDDEN)
