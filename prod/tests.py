from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Profile, Post, Like, FollowerCount
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@g.m", password='testpass')
        self.user.save()
        user_loged = User.objects.get(username="testuser")
        self.profile = Profile.objects.create(user=user_loged, id_user=user_loged.id)
        self.profile.save()

    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.bio, '')
        self.assertTrue(profile.profileimg.url.endswith('blank-profile-picture.png'))

    def test_profile_str(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), self.user.username)


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@g.m", password="testpass")
        self.user.save()
        self.post = Post.objects.create(
            user=self.user.username,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test caption',
            create_at=timezone.now(),
            user_img=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        )
        self.post.save()

    def test_post_creation(self):
        self.assertEqual(self.post.user, 'testuser')
        self.assertEqual(self.post.caption, 'Test caption')


class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@g.m", password="testpass")
        self.post = Post.objects.create(
            user=self.user.username,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test caption',
            create_at=timezone.now(),
            user_img=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        )
        self.like = Like.objects.create(
            id_post=str(self.post.id_post),
            user=self.user.username
        )

    def test_like_creation(self):
        self.assertEqual(self.like.id_post, str(self.post.id_post))
        self.assertEqual(self.like.user, 'testuser')


class FollowerCountModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass1')
        self.user2 = User.objects.create_user(username='user2', password='testpass2')
        self.follower_count = FollowerCount.objects.create(
            follower=self.user1.username,
            user=self.user2.username
        )

    def test_follower_count(self):
        self.assertEqual(self.follower_count.follower, 'user1')
        self.assertEqual(self.follower_count.user, 'user2')


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email="testuser@g.m",
            password='testpass'
        )
        self.user.save()
        user_loged = User.objects.get(username="testuser")
        self.profile = Profile.objects.create(user=user_loged, id_user=user_loged.id)
        self.profile.save()

    def test_index_view_logged_in(self):
        logged_in = self.client.login(username='testuser', password='testpass')
        self.assertTrue(logged_in)

        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_index_view_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_post_view(self):
        self.client.login(username='testuser', password='testpass')
        post = Post.objects.create(
            user=self.user.username,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test caption',
            create_at=timezone.now(),
            user_img=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        )
        response = self.client.get(reverse('post', args=[post.id_post]),follow=True)
        self.assertEqual(response.status_code, 200)

    def test_likes_view(self):
        self.client.login(username='testuser', password='testpass')
        post = Post.objects.create(
            user=self.user.username,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test caption',
            create_at=timezone.now(),
            user_img=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        )
        response = self.client.post(reverse('likes'), {'post_id': str(post.id_post)})
        self.assertEqual(response.status_code, 302)

    def test_search_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('search'), {'query': 'test'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_settings_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('settings'),follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_profile_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_profile'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_post_view(self):
        self.client.login(username='testuser', password='testpass')
        post = Post.objects.create(
            user=self.user.username,
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            caption='Test caption',
            create_at=timezone.now(),
            user_img=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
        )
        response = self.client.post(reverse('delete_post', args=[post.id_post]), follow=True)
        self.assertEqual(response.status_code, 200)
