from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Q, Sum, DecimalField
from django.db.models.functions import Cast

from django.conf import settings
from model_utils import Choices
from categories.models import Category

UserModel = settings.AUTH_USER_MODEL


####### Quizzes section
class Quiz(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
          return self.name

    def get_questions_count(self):
        return self.questions.count()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_title = models.TextField()
    question_extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
          return self.question_title

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
          return f'{self.question}-{self.choice}'


class QuizResult(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="quiz_result")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}-{self.quiz}'

    def save(self, *args, **kwargs):
        if self.selected_choice.is_correct:
            self.is_correct = True
        else:
            self.is_correct = False
        super(QuizResult, self).save(*args, **kwargs) # Call the "real" save() method.


class QuizAttempt(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_attempts")

    def __str__(self):
        return f'{self.user}-{self.quiz}'

####### Course Section
class Course(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, blank=True, null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
          return self.title

    def atomic_post_save(self, sender, created, **kwargs):
        CoursePrivacy.objects.get_or_create(course=self)


    def can_access(self, user):
        if self.privacy.is_public():
            return True
        elif self.privacy.is_private():
            return False
        else:
            return user in self.privacy.shared_with.all()

    def get_content_count(self):
        return self.content.count()

    def get_duration(self):
        duration = self.content.aggregate(sum=Sum('duration'))['sum']
        return duration


######### Course Content section
class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="content")
    title = models.CharField(max_length=100)
    description = models.TextField()
    video = models.FileField(upload_to='video', blank=True, null=True)
    audio = models.FileField(upload_to='audio', blank=True, null=True)
    text = models.TextField(blank=True, null=True, max_length=100)
    duration = models.IntegerField(blank=True, default=0)
    order = models.IntegerField()
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('order', )

    def __str__(self):
          return self.title

    def atomic_post_save(self, sender, created, **kwargs):
        ContentPrivacy.objects.get_or_create(content=self)

    def can_access(self, user):
        if self.privacy.is_public():
            return True
        elif self.privacy.is_private():
            return False
        else:
            return user in self.privacy.shared_with.all()



###### Course Activity Tracking
class CourseActivity(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='course_activity')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Courses Activity Tracker'

    def __str__(self):
          return f'{self.user.email}-{self.course.title}-{self.content.title}'


#### Comments and feedback section
class CourseCommentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(content=None, status='published')

class ContentCommentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(~Q(content=None), status='published')

class Comment(models.Model):

    STATUS_CHOICES = Choices(
        ('pending', 'Pending'),
        ('published', 'Published'),
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="comments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    comment_body = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES.pending)
    date_created = models.DateTimeField(auto_now_add=True)

    # Default manager
    objects = models.Manager()

    # Custom managers for comments
    course_comments = CourseCommentsManager()
    content_comments = ContentCommentsManager()


    def __str__(self):
        return f'{self.user.email}-{self.comment_body}'


class Feedback(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="feedbacks")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="feedbacks")
    rating = models.IntegerField(
    validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_rating",
                check=models.Q(rating__range=(1, 5)),
            ),
        ]

    def __str__(self):
          return f'{self.user.email}-{self.course.title}'


### User's Requests section
class CorrectInfo(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    min_from = models.CharField(blank=True, max_length=100)
    min_to = models.CharField(blank=True, max_length=100)
    scientific_evidence = models.TextField(blank=True)

    def __str__(self):
          return f'{self.user.email}-{self.course.title}-{self.content.title}'


class Report(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
          return f'{self.user.email}-{self.course.title}-{self.content.title}'


## Privacy section
class Privacy(models.Model):

    PRIVACY_CHOICES = Choices(
        ('public', 'Public'),
        ('private', 'Private'),
        ('custom', 'Custom'),
    )

    option = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default=PRIVACY_CHOICES.private)
    shared_with = models.ManyToManyField(UserModel, blank=True)

    def is_public(self):
        return self.option == self.PRIVACY_CHOICES.public

    def is_private(self):
        return self.option == self.PRIVACY_CHOICES.private

    def is_custom(self):
        return self.option == self.PRIVACY_CHOICES.custom



class CoursePrivacy(Privacy):

    course = models.OneToOneField(Course, on_delete=models.CASCADE, blank=True, related_name="privacy")

    def __str__(self):
          return self.course.title


class ContentPrivacy(Privacy):

    content = models.OneToOneField(Content, on_delete=models.CASCADE, blank=True, related_name="privacy")

    def __str__(self):
          return self.content.title

# Attachments section
class Attachement(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='attachements')


class CourseAttachement(Attachement):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="attachments")
    def __str__(self):
          return self.course.title

class ContentAttachement(Attachement):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="attachments")
    def __str__(self):
          return self.content.title
