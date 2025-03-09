import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        # テスト用のFlaskアプリケーションを設定
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        # インデックスページが正しく表示されるかをテスト
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)  # ステータスコードが200であることを確認
        self.assertIn('匿名掲示板'.encode('utf-8'), response.data)  # ページに「匿名掲示板」というテキストが含まれていることを確認

    def test_create_room(self):
        # 新しい部屋を作成する機能をテスト
        response = self.app.post('/create_room', data={'room_name': 'テスト部屋'})
        self.assertEqual(response.status_code, 302)  # リダイレクトが行われることを確認

    def test_room(self):
        # 特定の部屋のページが正しく表示されるかをテスト
        response = self.app.get('/room/1')  # 1番の部屋を取得
        self.assertEqual(response.status_code, 200)  # ステータスコードが200であることを確認
        self.assertIn('投稿一覧'.encode('utf-8'), response.data)  # ページに「投稿一覧」というテキストが含まれていることを確認

    def test_create_post(self):
        # 新しい投稿を作成する機能をテスト
        response = self.app.post('/room/1/create_post', data={'content': 'テスト投稿'})
        self.assertEqual(response.status_code, 302)  # リダイレクトが行われることを確認

if __name__ == '__main__':
    unittest.main() 