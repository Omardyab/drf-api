from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post

class PostModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='Omar',password='omarpass')
        test_user.save()
        test_post = Post.objects.create(
            owner = test_user,
            title = 'Austria',
            comments = 'Trip to Vienna'
        )
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post.owner), 'Omar')
        self.assertEqual(post.title, 'Austria')
        self.assertEqual(post.comments, 'Trip to Vienna')

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):
        test_user = get_user_model().objects.create_user(username='Omar',password='omarpass')
        test_user.save()
        test_post = Post.objects.create(
            owner = test_user,
            title = 'Austria',
            comments = 'Trip to Vienna'
        )
        test_post.save()
        response = self.client.get(reverse('posts_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_post.title,
            'comments': test_post.comments,
            'owner': test_user.id,
        })


    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()
        url = reverse('posts_list')
        data = {
            "title":"Berlin was a lot of Fun!",
            "comments":"Trip to Berlin was great",
            "owner":test_user.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()
        test_post = Post.objects.create(
            owner = test_user,
            title = 'Austria 2',
            comments = 'Trip to Vienna'
        )
        test_post.save()
        url = reverse('posts_detail',args=[test_post.id])
        data = {
            "title":"Berlin was a lot of Fun!",
            "comments":"Trip to Berlin was great",
            "owner":test_user.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, url)
        self.assertEqual(Post.objects.count(), test_post.id)
        self.assertEqual(Post.objects.get().title, data['title'])

    def test_delete(self):
        """Test the api can delete a post."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            owner = test_user,
            title = 'Austria',
            comments = 'Trip to Vienna'
        )
        test_post.save()
        post = Post.objects.get()
        url = reverse('posts_detail', kwargs={'pk': post.id})
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)