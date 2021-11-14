from django.conf import settings


# this function is for initializing profile image file path
def get_profile_image_path(self, filename):
    return f'{settings.PROFILE_IMAGES_URL}/{self.username}/{filename}'

# Not used
# this function is for getting the default profile image path
def get_default_profile_image():
    return f'{settings.PROFILE_IMAGES_URL}/avatar.png'
