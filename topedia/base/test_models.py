from django.test import TestCase
from .models import User, UserFollowing, Topic, LearningMaterial, Room, UserFavourites, Message

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='johndoe', name='John Doe', email='johndoe@gmail.com', bio='Welcome to my profile.', avatar=None)
    
    def test_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_bio_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')
    
    def test_avatar_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('avatar').verbose_name
        self.assertEqual(field_label, 'avatar')
    
    def test_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_avatar_default(self):
        user = User.objects.get(id=1)
        default_value = user._meta.get_field('avatar').default
        self.assertEqual(default_value, 'avatar.svg')

class UserFollowingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='markbrown', name='Mark Brown', email='markbrown@gmail.com', bio='Welcome to my profile.', avatar=None)
        user2 = User.objects.create(username='charliegreen', name='Charlie Green', email='charliegreen@gmail.com', bio='Welcome to my profile.', avatar=None)
        userfollowing = UserFollowing.objects.create(user=user1)
        userfollowing.following.set([user2])
    
    def test_user_label(self):
        userfollowing = UserFollowing.objects.get(id=1)
        field_label = userfollowing._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_following_label(self):
        userfollowing = UserFollowing.objects.get(id=1)
        field_label = userfollowing._meta.get_field('following').verbose_name
        self.assertEqual(field_label, 'following')

    def test_following_many_to_many(self):
        userfollowing = UserFollowing.objects.get(id=1)
        many_to_many = userfollowing._meta.get_field('following').many_to_many
        self.assertTrue(many_to_many, True)

    def test_following_blank(self):
        userfollowing = UserFollowing.objects.get(id=1)
        blank = userfollowing._meta.get_field('following').blank
        self.assertTrue(blank, True)
    
    def test_user1_follows_user2(self):
        userfollowing = UserFollowing.objects.get(id=1)
        user2 = User.objects.get(id=2)
        following = userfollowing.following.contains(user2)
        self.assertTrue(following, True)

class TopicTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Topic.objects.create(name='Python')
    
    def test_name_label(self):
        topic = Topic.objects.get(id=1)
        field_label = topic._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        topic = Topic.objects.get(id=1)
        max_length = topic._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

class LearningMaterialTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='jessicawhite', name='Jessica White', email='jessicawhite@gmail.com', bio='Welcome to my profile.', avatar=None)
        LearningMaterial.objects.create(user=user, heading='This is my heading', body='This is my body', image=None, video=None, footer='This is my footer')

    def test_user_label(self):
        material = LearningMaterial.objects.get(id=1)
        field_label = material._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
    
    def test_heading_label(self):
        material = LearningMaterial.objects.get(id=1)
        field_label = material._meta.get_field('heading').verbose_name
        self.assertEqual(field_label, 'heading')

    def test_body_label(self):
        material = LearningMaterial.objects.get(id=1)
        field_label = material._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')

    def test_image_label(self):
        material = LearningMaterial.objects.get(id=1)
        field_label = material._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_video_label(self):
        material = LearningMaterial.objects.get(id=1)
        field_label = material._meta.get_field('video').verbose_name
        self.assertEqual(field_label, 'video')

    def test_footer_label(self):
        material = LearningMaterial.objects.get(id=1)
        field_label = material._meta.get_field('footer').verbose_name
        self.assertEqual(field_label, 'footer')

    def test_heading_max_length(self):
        material = LearningMaterial.objects.get(id=1)
        max_length = material._meta.get_field('heading').max_length
        self.assertEqual(max_length, 200)
    
    def test_heading_default(self):
        material = LearningMaterial.objects.get(id=1)
        default_value = material._meta.get_field('heading').default
        self.assertEqual(default_value, '')
    
    def test_image_blank(self):
        material = LearningMaterial.objects.get(id=1)
        blank = material._meta.get_field('image').blank
        self.assertTrue(blank, True)

    def test_video_max_length(self):
        material = LearningMaterial.objects.get(id=1)
        max_length = material._meta.get_field('video').max_length
        self.assertEqual(max_length, 200)
    
    def test_video_blank(self):
        material = LearningMaterial.objects.get(id=1)
        blank = material._meta.get_field('video').blank
        self.assertTrue(blank, True)
    
    def test_footer_blank(self):
        material = LearningMaterial.objects.get(id=1)
        blank = material._meta.get_field('footer').blank
        self.assertTrue(blank, True)

class RoomTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='issacsmith', name='Issac Smith', email='issacsmith@gmail.com', bio='Welcome to my profile.', avatar=None)
        user2 = User.objects.create(username='borisgown', name='Boris Gown', email='borisgown@gmail.com', bio='Welcome to my profile.', avatar=None)
        material = LearningMaterial.objects.create(user=user1, heading='This is my heading', body='This is my body', image=None, video=None, footer='This is my footer')
        topic = Topic.objects.create(name='JavaScript')
        room = Room.objects.create(host=user1, topic=topic, name="Let's Learn JavaScript!", description='This is my topic room!')
        room.participants.set([user2])
        room.learningMaterial.set([material])

    def test_host_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('host').verbose_name
        self.assertEqual(field_label, 'host')
    
    def test_topic_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('topic').verbose_name
        self.assertEqual(field_label, 'topic')
    
    def test_name_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_description_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')
    
    def test_participants_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('participants').verbose_name
        self.assertEqual(field_label, 'participants')
    
    def test_learningMaterial_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('learningMaterial').verbose_name
        self.assertEqual(field_label, 'learningMaterial')
    
    def test_name_max_length(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
    
    def test_description_blank(self):
        room = Room.objects.get(id=1)
        blank = room._meta.get_field('description').blank
        self.assertTrue(blank, True)
    
    def test_participants_blank(self):
        room = Room.objects.get(id=1)
        blank = room._meta.get_field('participants').blank
        self.assertTrue(blank, True)
    
    def test_room_has_participant(self):
        room = Room.objects.get(id=1)
        user2 = User.objects.get(id=2)
        participant = room.participants.contains(user2)
        self.assertTrue(participant, True)
    
    def test_room_has_learningMaterial(self):
        room = Room.objects.get(id=1)
        material = LearningMaterial.objects.get(id=1)
        learningMaterial = room.learningMaterial.contains(material)
        self.assertTrue(learningMaterial, True)

class UserFavouritesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='jackturner', name='Jack Turner', email='jackturner@gmail.com', bio='Welcome to my profile.', avatar=None) 
        topic = Topic.objects.create(name='Java')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn Java!", description='This is my topic room!')
        favourites = UserFavourites.objects.create(user=user)
        favourites.rooms.set([room])

    def test_user_label(self):
        favourites = UserFavourites.objects.get(id=1)
        field_label = favourites._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
    
    def test_rooms_label(self):
        favourites = UserFavourites.objects.get(id=1)
        field_label = favourites._meta.get_field('rooms').verbose_name
        self.assertEqual(field_label, 'rooms')

    def test_UserFavourites_has_room(self):
        room = Room.objects.get(id=1)
        favourites = UserFavourites.objects.get(id=1)
        userFavourites = favourites.rooms.contains(room)
        self.assertTrue(userFavourites, True)    

class MessageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='joshsparrow', name='Josh Sparrow', email='joshsparrow@gmail.com', bio='Welcome to my profile.', avatar=None) 
        topic = Topic.objects.create(name='c#')
        room = Room.objects.create(host=user, topic=topic, name="Let's Learn c#!", description='This is my topic room!')
        Message.objects.create(user=user, room=room, body='This is my body')

    def test_user_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
    
    def test_room_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('room').verbose_name
        self.assertEqual(field_label, 'room')
    
    def test_body_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'body')