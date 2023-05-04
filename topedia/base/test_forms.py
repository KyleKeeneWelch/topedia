from django.test import TestCase
from .forms import RoomForm, LoginForm, RegisterForm, UserForm, MaterialForm

class RoomFormTest(TestCase):
    def test_name_label(self):
        form = RoomForm()
        self.assertTrue(form.fields['name'].label is None or 
        form.fields['name'].label == 'Name')
    
    def test_description_label(self):
        form = RoomForm()
        self.assertTrue(form.fields['description'].label is None or 
        form.fields['description'].label == 'Description')
    
class LoginFormTest(TestCase):
    def test_email_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['email'].label is None or 
        form.fields['email'].label == 'Email')
    
    def test_password_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['password'].label is None or 
        form.fields['password'].label == 'Password')

class RegisterFormTest(TestCase):
    def test_name_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['name'].label is None or 
        form.fields['name'].label == 'Name')
    
    def test_username_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['username'].label is None or 
        form.fields['username'].label == 'Username')
    
    def test_email_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['email'].label is None or 
        form.fields['email'].label == 'Email')
    
    def test_bio_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['bio'].label is None or 
        form.fields['bio'].label == 'Bio')
    
    def test_avatar_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['avatar'].label is None or 
        form.fields['avatar'].label == 'Avatar')
    
    def test_password_label(self):
        form = RegisterForm()
        self.assertTrue(form.fields['password'].label is None or 
        form.fields['password'].label == 'Password')

class UserFormTest(TestCase):
    def test_name_label(self):
        form = UserForm()
        self.assertTrue(form.fields['name'].label is None or 
        form.fields['name'].label == 'Name')
    
    def test_username_label(self):
        form = UserForm()
        self.assertTrue(form.fields['username'].label is None or 
        form.fields['username'].label == 'Username')
    
    def test_email_label(self):
        form = UserForm()
        self.assertTrue(form.fields['email'].label is None or 
        form.fields['email'].label == 'Email')
    
    def test_bio_label(self):
        form = UserForm()
        self.assertTrue(form.fields['bio'].label is None or 
        form.fields['bio'].label == 'Bio')
    
    def test_avatar_label(self):
        form = UserForm()
        self.assertTrue(form.fields['avatar'].label is None or 
        form.fields['avatar'].label == 'Avatar')
    
    def test_password_label(self):
        form = UserForm()
        self.assertTrue(form.fields['password'].label is None or 
        form.fields['password'].label == 'Password')

class MaterialFormTest(TestCase):
    def test_heading_label(self):
        form = MaterialForm()
        self.assertTrue(form.fields['heading'].label is None or 
        form.fields['heading'].label == 'Heading')

    def test_body_label(self):
        form = MaterialForm()
        self.assertTrue(form.fields['body'].label is None or 
        form.fields['body'].label == 'Body')

    def test_image_label(self):
        form = MaterialForm()
        self.assertTrue(form.fields['image'].label is None or 
        form.fields['image'].label == 'Image')

    def test_video_label(self):
        form = MaterialForm()
        self.assertTrue(form.fields['video'].label is None or 
        form.fields['video'].label == 'Video')

    def test_footer_label(self):
        form = MaterialForm()
        self.assertTrue(form.fields['footer'].label is None or 
        form.fields['footer'].label == 'Footer')