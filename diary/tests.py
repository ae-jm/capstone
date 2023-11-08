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

    def test_post_detail(self):
        # 1.1 Post가 하나 있다.
        post_001 = Post.objects.create(
            title='첫번째포스트',
            content='111111111111111111111111'
        )
        # 1.2 그 포스트의 url은 'post/1/' 이다.
        self.assertEqual(post_001.get_absoulute_url(), 'post/1/')
        # 2. 첫번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번째 post url로 접근하면 정상적으로 작동한다.
        response = self.client.get(post_001.get_absoulute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        navbar = soup.nav
        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(post_001.title, soup.title.text)
        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        # 2.5 첫 번째 포스트의 작성자가 포스트 영역에 있다
        # 2.6 첫 번째 포스트의 내용이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)

    def test_create_post(self):
        response = self.client.get('/post/create_new/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/post/create_new/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')
        self.asserrIn('Create New post', main_area.text)

        self.client.post(
            '/post/create_new/',
            {
                'title': 'Post Form 만들기',
                'content':'Post Form 페이지를 만듭시다.',
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, 'Post Form 만들기')

    def test_update_post(self):
        update_post_url = f'/post/update_post/{self.post_003.pk}/'

        #로그인하지 않은 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        #로그인은 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(
            username=self.user_trump.username,
            password='somepassword'
        )
        reponse = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        #작성자가 접근하는 경우
        self.client.login(
            username = self.post_003.author.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        response = self.client.post(
            update_post_url,
            {
                'title':'세 번째 포스트를 수정했습니다. ',
                'content':'안녕 세계? 우리는 하나!',
            },
            follow=True
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)