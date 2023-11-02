from django.test import TestCase, Client
from bs4 import BeautifulSoup
from . models import Post

class TestView(TestCase):
    def setup(self):
        self.client = Client()

    def test_post(self):
        # 1.1 포스트 목록 페이지 가져온다.
        response = self.client.get('/post/')
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지 타이틀은 'post'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'mudi')
        # 1.4 네비게이션 바가 있다.
        navbar = soup.nav
        # 2.1 포스트(게시물)이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # 2.2 main area에 '아직 게시물이 없습니다.' 라는 문구가 나타난다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        # 3.1 포스트가 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content='Hello World. We are the world.',
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='1등이 전부는 아니잖아요?',
        )
        self.assertEqual(Post.objects.count(), 2)
        # 3.2 포스트 목록 페이지를 새로고침 했을 때
        response = self.client.get('/post/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        # 3.3 main area에 포스트 2개의 제목이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 '아직 게시물이 없습니다.' 라는 문구 더이상 나타나지 x
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

    def test_create_post(self):
        response = self.client.get('/post/newpost/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('New Post', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.asserrIn('Create New post', main_area.text)