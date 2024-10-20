from django.test import TestCase
from django.contrib.auth.models import User
from users.models import TravelPlan
from allauth.socialaccount.models import SocialAccount
from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError

class TravelPlanTestCase(TestCase):
    # Create mock user for testing
    @classmethod
    def setUpTestData(cls):
        # Create a user that simulates a Google OAuth user
        cls.user = User.objects.create_user(
            username='testuser@example.com',
            email='testuser@example.com',
            password='12345'
        )
        # Create a social account for the user
        SocialAccount.objects.create(
            user=cls.user,
            provider='google',
            uid='123456789',
            extra_data={}
        )
        # Verify the email
        EmailAddress.objects.create(
            user=cls.user,
            email=cls.user.email,
            verified=True,
            primary=True
        )

    def test_create_travel_plan(self):
        plan_name = 'Test Plan'
        
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            plan_name=plan_name,
            group_size=2,
            trip_description='A test trip',
            primary_group_code='TEST123'
        )
        self.assertEqual(travel_plan.user, self.user)
        self.assertEqual(travel_plan.plan_name, plan_name)

    def test_user_can_have_multiple_plans(self):
        TravelPlan.objects.create(
            user=self.user,
            plan_name='Plan 1',
            group_size=2,
            trip_description='First trip',
            primary_group_code='TEST1'
        )
        TravelPlan.objects.create(
            user=self.user,
            plan_name='Plan 2',
            group_size=3,
            trip_description='Second trip',
            primary_group_code='TEST2'
        )
        user_plans = TravelPlan.objects.filter(user=self.user)
        self.assertEqual(user_plans.count(), 2)

    def test_long_plan_name(self):
        max_length = TravelPlan._meta.get_field('plan_name').max_length
        long_plan_name = 'x' * (max_length + 1)
        
        travel_plan = TravelPlan(
            user=self.user,
            plan_name=long_plan_name,
            group_size=2,
            trip_description='A test trip',
            primary_group_code='TEST123'
        )
        
        with self.assertRaises(ValidationError):
            travel_plan.full_clean()

    def test_no_plan_name(self):
        no_plan_name = ''
        travel_plan = TravelPlan(
            user=self.user, 
            plan_name=no_plan_name, 
            group_size=2, 
            trip_description='A test trip', 
            primary_group_code='TEST123'
        )
        
        with self.assertRaises(ValidationError):
            travel_plan.full_clean()
