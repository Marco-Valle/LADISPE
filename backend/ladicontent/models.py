from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from tinymce.models import HTMLField
from filebrowser.fields import FileBrowseField
from phonenumber_field.modelfields import PhoneNumberField


User = settings.AUTH_USER_MODEL


class LADINews(models.Model):
    """LADINews db model."""

    timestamp = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to='news/%Y/%m/%d/', default='default.png')
    title = models.CharField(max_length=50)
    link = models.URLField(max_length=200, blank=True, null=True)
    in_evidence = models.BooleanField(default=False)
    text = models.TextField(blank=True, help_text="Use &lt;br&gt; to break the line")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.title, self.owner)

    class Meta:
        verbose_name_plural = 'Ladi news'


class LADIGallery(models.Model):
    """LADIGallery db model."""

    title = models.CharField(   max_length=30, 
                                unique=True, 
                                help_text="REMARK:<br>If you want to display a gallery in the home, create a gallery named Home"
                            )
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.title, self.owner)


class LADIPicture(models.Model):
    """
    LADIPicture db model
    Galleries' pictures (not accessible from the file browser)
    They can be linked to a news (ex. homepage) or with an external link (not both).
    """
    
    timestamp = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to='gallery/%Y/%m/%d/')
    gallery = models.ForeignKey(LADIGallery, on_delete=models.CASCADE, blank=True, null=True,
                                help_text="Select the gallery where you want to show the picture")
    link = models.URLField(max_length=200, blank=True, null=True, help_text="Link to be redirected on click")
    description = models.TextField(blank=True)
    news = models.ForeignKey(LADINews, on_delete=models.SET_NULL, null=True, blank=True,
                             help_text="You can link the picture to a news (link redirection won't work)")

    def __str__(self) -> str:
        string = 'Picture - {}'.format(self.gallery)
        if self.description != '':
            string += '- {}'.format(self.description)
        return string


class LADIStory(models.Model):
    """LADIStory db model."""

    STORY_TYPES = (
        (1, 'Story'),
        (2, 'Material'),
    )

    timestamp = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    type = models.IntegerField(choices=STORY_TYPES, default=1)
    cover = FileBrowseField("Image", max_length=200, directory='Covers/', default='default.png')
    html = HTMLField(blank=True)
    preview = models.TextField(blank=True)
    author = models.CharField(max_length=30, blank=True)
    quote = models.CharField(max_length=30, blank=True)
    gallery = models.ForeignKey(LADIGallery, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    def __str__(self) -> str:
        return '{} - {} - {}'.format(self.type, self.title, self.owner)


class LADIStaff(models.Model):
    """LADIStaff db model."""

    cover = models.ImageField(upload_to='staff/%Y/%m/%d/', default='default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,
                                help_text="If you create a LADIStaff with a particular user, his name, surname and email will be public")
    position = models.CharField(max_length=30)
    phone = PhoneNumberField(null=True, blank=True)
    fax = PhoneNumberField(null=True, blank=True)

    def __str__(self) -> str:
        return '{}'.format(self.user)


class LADIForm(models.Model):
    """LADIForm db model."""

    title = models.CharField(max_length=70, blank=False, unique=True)
    file = models.FileField(upload_to='forms/')
    public = models.BooleanField(default=True)

    def __str__(self) -> str:
        return '{}'.format(self.title)