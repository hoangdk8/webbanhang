import pytest
from app.models import Category, Product,Order,OrderItem
from django.urls import reverse
from django.test import Client,TestCase
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(name='test product', price='123', digital=True)
    assert Product.objects.count() == 1
    assert product.name == 'test product'
    assert product.price == '123'
    assert product.digital == True
    assert product is not None

@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="Test Category", slug="test-category")
    assert category is not None

@pytest.mark.django_db
def test_register_view():
    client = Client() #Dòng này tạo một đối tượng Client để thực hiện các yêu cầu HTTP giả lập
    username = 'testuser'
    password = 'testpassword'
    #thực hiện một yêu cầu HTTP POST đến URL được xác định bởi reverse('register'), 
    # nghĩa là URL được đặt tên là "register" trong ứng dụng của bạn. 
    # Dữ liệu đăng ký (tên người dùng và mật khẩu) được đính kèm trong dấu ngoặc nhọn và gửi đến server.
    # Kết quả của yêu cầu sẽ được lưu trong biến response.
    response = client.post(reverse('register'), {'username': username, 'password1': password, 'password2': password})
    #Dòng này kiểm tra rằng mã trạng thái HTTP của phản hồi là 302, 
    # có nghĩa là sau khi đăng ký thành công, 
    # người dùng sẽ được chuyển hướng đến một trang khác (thường là trang đăng nhập).
    assert response.status_code == 302
    #kiểm tra xem có một bản ghi người dùng trong cơ sở dữ liệu với tên người dùng đã đăng ký (username) hay không. 
    # Nếu User.objects.filter(username=username).exists() là True, 
    # điều này có nghĩa rằng đăng ký đã thành công và tên người dùng đã được lưu trong cơ sở dữ liệu.
    assert User.objects.filter(username=username).exists()

@pytest.mark.django_db
def test_login_view():
    client = Client()
    username = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)
    response = client.post(reverse('login'), {'username': username, 'password': password})
    assert response.status_code == 302
    #kiểm tra rằng id của người dùng (_auth_user_id) đã đăng nhập
    #trùng khớp với id của người dùng được tạo (user.id) sau khi đăng nhập thành công.
    #client.session['_auth_user_id'] là cách để truy cập giá trị _auth_user_id trong phiên của người dùng.
    #str(user.id) chuyển đổi id của người dùng từ kiểu dữ liệu integer sang kiểu dữ liệu string để so sánh.
    assert client.session['_auth_user_id'] == str(user.id)

@pytest.mark.django_db
def test_logout_view():
    client = Client()
    response = client.get(reverse('logout'))
    assert response.status_code == 302  # Kiểm tra xem sau khi đăng xuất, người dùng có được chuyển hướng không
    assert '_auth_user_id' not in client.session  # Kiểm tra xem người dùng đã đăng xuất hay chưa
    
@pytest.mark.django_db
class OrderModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpassword'
        )
        # Create a test order
        self.order = Order.objects.create(
            customer=self.user,
            transaction_id='123'
        )
        # tạo 1 test product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.0
        )
        # Tạo test order item
        self.order_item = OrderItem.objects.create(
            product=self.product,
            order=self.order,
            quantity=2
        )
    def test_order_str_method(self):
        self.assertEqual(str(self.order), str(self.order.id))

    def test_get_cart_item(self):
        self.assertEqual(self.order.get_cart_item, 2)  # số lượng sản phẩm trong giỏ hàng

    def test_get_cart_total(self):
        self.assertEqual(self.order.get_cart_total, 20.0)  # 2 items * $10 

    def test_order_item_get_total(self):
        self.assertEqual(self.order_item.get_total, 20.0)  # 2 items * $10 
