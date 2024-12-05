from django.test import TestCase
from .models import BoardModel
from django.urls import reverse
from django.contrib.auth.models import User

#userと保存データを指定し、保存
class BoardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        obj = BoardModel(title = "タイトルです" ,content="コンテンツです",place = "場所です",user=self.user)
        obj.save()

# データが正しく保存されているか
    def test_saved_single_object(self):
        qs_counter = BoardModel.objects.count()
        self.assertEqual(qs_counter,1)
#createで作れるか
    def test_create_on_createView(self):
        url = reverse('board-create')
        create_data = {"title":"title作成","content":"コンテンツ","place":"場所"}
        response = self.client.post(url,create_data)
        qs_counter2 = BoardModel.objects.count()
        self.assertEqual(response.status_code,302)
        self.assertEqual(qs_counter2,2)

#queryが存在しない時、４０４エラーを返すか
    def test_response_404(self):
        detail_url = reverse('board-detail',kwargs={'pk':100})
        detail_response = self.client.get(detail_url)
        self.assertEqual(detail_response.status_code,404)