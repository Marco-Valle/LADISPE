from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from filebrowser.fields import FileBrowseField
from tinymce.models import HTMLField


User = settings.AUTH_USER_MODEL


class LADICourse(models.Model):
    """LADICourse db model."""

    timestamp = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)
    private_email = models.BooleanField(default=False)
    mandatory_redirection = models.BooleanField(default=False, help_text="""Set to True if you want to disable the LADICourse page and instead
                                                redirect to the official site when Open is clicked (course site field is required).""")
    course_code = models.CharField(max_length=7, unique=True,
                                   validators=[RegexValidator('^[0-9]{2}[A-Z]{5}$', 'Course code in the format ##XXXXX')])
    cover = FileBrowseField("Image", max_length=200, directory='Covers/', default='default.png')
    title = models.CharField(max_length=60, unique=True)
    degree_course = models.CharField(max_length=80, blank=True)
    course_site = models.URLField(blank=True, help_text="URL of the official site of the course (required if mandatory redirection is enabled).")
    description = models.TextField(blank=True, help_text="Use &lt;br&gt; to break the line")
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    first_assistant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='first_assistant', null=True, blank=True)
    second_assistant = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='second_assistant', null=True, blank=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.course_code, self.title)


class LADILecture(models.Model):
    """LADILecture db model."""

    timestamp = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(LADICourse, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    cover = FileBrowseField("Image", max_length=200, directory='Covers/', default='default.png')
    lecture_url = models.URLField(blank=True, help_text="URL to be opened insted of the standard LADISPE site page.")
    html = HTMLField(blank=True)
    author = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.course, self.title)
