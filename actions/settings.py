from django.conf import settings

actions_types = getattr(settings, 'ACTIONS_TYPES', (
    ('enroll_course', 'Enrolled'),
    ('favorite_course', 'Added to Favorites'),
    ('watched', 'Have Watched'),
))

allowed_actions_models = getattr(settings, 'ALLOWED_ACTIONS_MODELS', (
    ('enroll_course', 'Enrolled'),
    ('favorite_course', 'Added to Favorites'),
    ('watched', 'Have Watched'),
))
