from django.db import models
from django.db.models import Q
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.


class PostQuerySet(models.QuerySet):
    def browser(self, query=None):
        qs= self
        if query is None:
            or_lookup = (Q(content__icontains=query),
                         Q(author__icontains=query),
                        )
            qs= qs.filter(or_lookup).distinct()
        return qs

class PostManager(models.Manager):
    def browser(self):
        return PostQuerySet(self.model, using=self._db)
    
    def browser(self, query=None):
        return self._get_queryset().browser(query=query)

        # qs = self.get_queryset()
        # if query is not None:
        #     or_lookup = (Q(content__icontains=query), 
        #                  Q(author__icontains=query)
        #                 )
        #     qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        # return qs



class Post(models.Model):
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    objects = PostManager()

    def __str__(self):
        return str(self.content[:20])

    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self):
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

    


    