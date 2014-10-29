from django.db import models
from django.core.files import File
from os.path import join
from PIL import Image as PImage
import os
# from string import join as pjoin
from tempfile import *

# Create your models here.

class Album(models.Model):
    title = models.CharField(max_length=60)

    def __unicode__(self):
        return self.title

    def images(self):
        lst = [x.image.name for x in self.image_set.all()]
        lst = ["<a href='/i/%s'>%s</a>" % (x, x.split('/')[-1]) for x in lst]
        return join(lst, ', ')

    images.allow_tags = True

class Tag(models.Model):
	tag = models.CharField(max_length=50)

	def __unicode__(self):
		return self.tag

class Image(models.Model):
    """all necessary data for Image"""
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to="i/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    taken = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=True, null=True)
    hidden_rating = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="i/", blank=True, null=True)
    thumbnail2 = models.ImageField(upload_to="i/", blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

        im = PImage.open(self.image.name)
        self.width, self.height = im.size

        # large thumbnail
        fn, ext = os.path.splitext(self.image.name)
        im.thumbnail((200,200), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb2" + ext
        tf2 = NamedTemporaryFile()
        im.save(tf2.name, "JPEG")
        self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
        tf2.close()

        # small thumbnail
        im.thumbnail((100,100), PImage.ANTIALIAS)
        thumb_fn = fn + "-thumb" + ext
        tf = NamedTemporaryFile()
        im.save(tf.name, "JPEG")
        self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
        tf.close()

        super(Image, self).save(*args, ** kwargs)

    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def __unicode__(self):
	    return self.image.name

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        return str(join(lst, ', '))

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return str(join(lst, ', '))

    def thumbnail_(self):
    	return '<img border="0" alt="" src="http://localhost:8001/%s"/>' % self.thumbnail2.name
        # return """<a href="/%s"><img border="0" alt="" src="/%s" height="40" /></a>""" % (
        #                                                             (self.thumbnail.name, self.thumbnail.name))
    thumbnail_.allow_tags = True

