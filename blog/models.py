from tkinter import CASCADE
from django.db import models
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length= 50)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length= 250)
    body = models.TextField()
    author = models.ForeignKey('Author', on_delete= models.CASCADE)    
    date_created = models.DateTimeField(default= timezone.now)

    def copy(self):

        # print(BlogPost.objects.all())
        # Create A new blog using old contents and a new primary key
        newBlogPost = BlogPost.objects.get(pk= self.pk)
        newBlogPost.pk = None
        newBlogPost.save()
        # print(BlogPost.objects.all())

        # Create new comments corresponding to each comment of the post
        newComments = []
        for comment in self.comment_set.all():
            newComments.append(comment.copy())

        # Assign new comments to the BlogPost object
        newBlogPost.comment_set.set(newComments)
        newBlogPost.date_created = timezone.now()
        newBlogPost.save()
        # print(BlogPost.objects.all())

        return newBlogPost.pk

    def __str__(self):
        return "pk:{},{}:{}".format(self.pk, self.title, self.author)

class Comment(models.Model):
    blog_post = models.ForeignKey('BlogPost', on_delete= models.CASCADE)  
    text = models.TextField(max_length= 500)

    def copy(self):
        # print(Comment.objects.all())
        newComment = Comment.objects.get(pk= self.pk)
        newComment.pk = None
        newComment.save()
        # print(Comment.objects.all())
        return newComment

    def __str__(self):
        return "pk:{}, {}/{}".format(self.pk, self.text, self.blog_post)