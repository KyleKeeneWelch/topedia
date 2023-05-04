from django.test import TestCase
from django.urls import reverse
from .forms import LoginForm, RegisterForm, RoomForm, MaterialForm, UserForm
from .models import Room, Topic, Message, User, UserFavourites, LearningMaterial, UserFollowing

class LoginPageViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')

    def test_page_is_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page' in response.context)
        self.assertTrue(response.context['page'] == 'login')
    
    def test_form_is_loginForm(self):
        form = str(LoginForm())
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn(form, str(response.context['form']))

class LogoutUserViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302) #Was 200 then found out 302 means temporary moved aka redirected.

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_home(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

class RegisterPageViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/login_register.html')
    
    def test_form_is_registerForm(self):
        form = str(RegisterForm())
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn(form, str(response.context['form']))

class HomeViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_rooms_is_room(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rooms' in response.context)
        self.assertTrue(response.context['rooms'].model is Room)
    
    def test_topics_is_topic(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('topics' in response.context)
        self.assertTrue(response.context['topics'].model is Topic)
    
    def test_room_count_is_int(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('room_count' in response.context)
        self.assertEqual(type(response.context['room_count']), int)

    def test_room_messages_is_message(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('room_messages' in response.context)
        self.assertTrue(response.context['room_messages'].model is Message)

    def test_favourites_is_room(self):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        favourites = UserFavourites.objects.create(user=user)
        favourites.rooms.set([room])


        user = self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('favourites' in response.context)
        self.assertEqual(response.context['favourites'].model, Room)

class RoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        room.participants.set([user])
        favourites = UserFavourites.objects.create(user=user)
        favourites.rooms.set([room])
        material = LearningMaterial.objects.create(user=user, heading="This is a heading", body="This is a body")
        room.learningMaterial.set([material])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/room/1')
        self.assertEqual(response.status_code, 301) #Was 200 but permanentmly redirected so 301

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('room', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/room.html')

    def test_room_is_room(self):
        room = Room.objects.get(id=1)
        response = self.client.get(reverse('room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('room' in response.context)
        self.assertEqual(response.context['room'], room)

    def test_room_messages_is_message(self):
        response = self.client.get(reverse('room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('room_messages' in response.context)
        self.assertTrue(response.context['room_messages'].model is Message)
    
    def test_participants_is_user(self):
        response = self.client.get(reverse('room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('participants' in response.context)
        self.assertTrue(response.context['participants'].model is User)

    def test_favourites_is_room(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('favourites' in response.context)
        self.assertEqual(response.context['favourites'].model, Room)

    def test_learningMaterial_is_learningMaterial(self):
        material = LearningMaterial.objects.get(id=1)
        response = self.client.get(reverse('room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('learningMaterial' in response.context)
        self.assertIn(material, response.context['learningMaterial'])

class ShowFavouritesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        favourites = UserFavourites.objects.create(user=user)
        favourites.rooms.set([room])

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/favourites/1')
        self.assertEqual(response.status_code, 302) #Was 200 but temporarily redirected so 302

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('show-favourites', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('show-favourites', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/favourites.html')

    def test_user_is_user(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        user = User.objects.get(id=1)
        response = self.client.get(reverse('show-favourites', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.context)
        self.assertEqual(response.context['user'], user)

    def test_rooms_is_room(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('show-favourites', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rooms' in response.context)
        self.assertEqual(response.context['rooms'].model, Room)

class ShowFollowersViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        user2 = User.objects.create(username='borisgown', name='Boris Gown', email='borisgown@gmail.com', bio='Welcome to my profile.')
        following = UserFollowing.objects.create(user=user)
        following.following.set([user2])

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/following/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('show-following'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('show-following'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/following.html')  

    def test_following_is_user(self):
        user = User.objects.get(id=2)
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('show-following'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('following' in response.context)
        self.assertIn(user, response.context['following'])

class UserProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        favourites = UserFavourites.objects.create(user=user)
        favourites.rooms.set([room])
        user2 = User.objects.create(username='borisgown', name='Boris Gown', email='borisgown@gmail.com', bio='Welcome to my profile.')
        following = UserFollowing.objects.create(user=user)
        following.following.set([user2])

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/profile/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('user-profile', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('user-profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/profile.html') 

    def test_user_is_user(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        user = User.objects.get(id=1)
        response = self.client.get(reverse('user-profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.context)
        self.assertEqual(response.context['user'], user) 

    def test_rooms_is_room(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('user-profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('rooms' in response.context)
        self.assertEqual(response.context['rooms'].model, Room)

    def test_room_messages_is_message(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('user-profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('room_messages' in response.context)
        self.assertTrue(response.context['room_messages'].model is Message)

    def test_topics_is_topic(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('user-profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('topics' in response.context)
        self.assertTrue(response.context['topics'].model is Topic)

    def test_following_is_true(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('user-profile', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('following' in response.context)
        self.assertEquals(response.context['following'], True)

    def test_favourites_is_room(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('user-profile', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('favourites' in response.context)
        self.assertEqual(response.context['favourites'].model, Room)

class SetFavouriteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/set-favourite/1')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('set-favourite', args=[1]))
        self.assertEqual(response.status_code, 302)

class CreateRoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        Topic.objects.create(name='JavaScript')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/create-room/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('create-room'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('create-room'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/display_form.html')

    def test_form_is_roomform(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        form = str(RoomForm())
        response = self.client.get(reverse('create-room'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn(form, str(response.context['form']))

    def test_formName_is_createRoom(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('create-room'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn('createRoom', response.context['formName'])

    def test_topics_is_topic(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('create-room'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('topics' in response.context)
        self.assertTrue(response.context['topics'].model is Topic)

class CreateMaterialViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/create-material/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('create-material', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('create-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/display_form.html')

    def test_form_is_materialform(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        form = str(MaterialForm())
        response = self.client.get(reverse('create-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn(form, str(response.context['form']))

    def test_formName_is_createMaterial(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('create-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn('createMaterial', response.context['formName'])

class UpdateUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/update-user')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-user'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/display_form.html')

    def test_form_is_userform(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        user = User.objects.get(id=1)
        form = str(UserForm(instance=user))
        response = self.client.get(reverse('update-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn(form, str(response.context['form']))

    def test_formName_is_updateUser(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-user'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn('updateUser', response.context['formName'])

class UpdateMaterialViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        material = LearningMaterial.objects.create(user=user, heading="This is a heading", body="This is a body")
        room.learningMaterial.set([material])

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/update-material/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-material', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/display_form.html')

    def test_form_is_materialform(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        material = LearningMaterial.objects.get(id=1)
        form = str(MaterialForm(instance=material))
        response = self.client.get(reverse('update-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn(form, str(response.context['form']))

    def test_formName_is_updateMaterial(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn('updateMaterial', response.context['formName'])

class UpdateRoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/update-room/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-room', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/display_form.html')

    def test_form_is_roomform(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        room = Room.objects.get(id=1)
        form = str(RoomForm(instance=room))
        response = self.client.get(reverse('update-room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn(form, str(response.context['form']))

    def test_formName_is_updateRoom(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertIn('updateRoom', response.context['formName'])

    def test_topics_is_topic(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('update-room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('topics' in response.context)
        self.assertTrue(response.context['topics'].model is Topic)

class DeleteRoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/delete-room/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-room', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/delete.html')

    def test_obj_is_room(self):
        room = Room.objects.get(id=1)
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-room', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('obj' in response.context)
        self.assertEqual(response.context['obj'], room)

class DeleteMessageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        Message.objects.create(user=user, room=room, body="This is a message")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/delete-message/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-message', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-message', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/delete.html')

    def test_obj_is_message(self):
        message = Message.objects.get(id=1)
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-message', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('obj' in response.context)
        self.assertEqual(response.context['obj'], message)

class RemoveFavouriteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        favourites = UserFavourites.objects.create(user=user)
        favourites.rooms.set([room])

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/remove-favourite/1')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('remove-favourite', args=[1]))
        self.assertEqual(response.status_code, 302)

class UnfollowViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        user2 = User.objects.create(username='borisgown', name='Boris Gown', email='borisgown@gmail.com', bio='Welcome to my profile.')
        following = UserFollowing.objects.create(user=user)
        following.following.set([user2])        

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.post('/unfollow/2')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.post(reverse('unfollow', args=[2]))
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_home(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.post(reverse('unfollow', args=[2]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show-following'))

class DeleteMaterialViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        material = LearningMaterial.objects.create(user=user, heading="This is a heading", body="This is a body")
        room.learningMaterial.set([material])

    def test_view_url_exists_at_desired_location(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get('/delete-material/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-material', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/delete.html')

    def test_obj_is_heading(self):
        material = LearningMaterial.objects.get(id=1)
        self.client.login(email='johndoe@gmail.com', password='pass')
        response = self.client.get(reverse('delete-material', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('obj' in response.context)
        self.assertEqual(response.context['obj'], material.heading)

class TopicsPageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        topic = Topic.objects.create(name='JavaScript')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/topics/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('topics'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('topics'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/topics.html')

    def test_topics_is_topic(self):
        response = self.client.get(reverse('topics'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('topics' in response.context)
        self.assertTrue(response.context['topics'].model is Topic)

class ActivityPageViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='johndoe', password="pass", name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        Message.objects.create(user=user, room=room, body="This is a message")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/activity/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('activities'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('activities'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/activity.html')

    def test_room_messages_is_message(self):
        response = self.client.get(reverse('activities'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('room_messages' in response.context)
        self.assertTrue(response.context['room_messages'].model is Message)