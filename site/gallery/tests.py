from django.test import TestCase
from gallery.models import Image

# Create your tests here.

class ImageTests(TestCase):
	"""tests for PictureTests"""
	
	def test_add(self):
			image=Image(title="iMac")
			self.assertEquals(image.title, "iMac")