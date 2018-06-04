import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

def create_question(question_text, days):
    """
    Create a question with the given question text and published the given number of
    days offset until now... negative for questions published in the past, postitive
    for questions that have yet to be published.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):
    # test case methods must begin with test_
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently should return False for questions whose pub_date
        is in the future
        """
        future_question = create_question("Sample Question", 30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published recently should return False for questions whose pub_date
        is greater than one day ago
        """
        old_question = create_question("Sample Question", -30)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently should return True for questions whose pub_date
        is within one day
        """
        recent_question = create_question("Sample Question", 0)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed
        """

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No questions are available.")
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page
        """
        create_question("Sample Question", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Sample Question>']
        )

    def test_future_question(self):
        """
        Question with a pub_date in the future are not displayed on the index page
        """
        create_question("Sample Question", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
        response.context['latest_questions'],
        []
        )

    def test_limit_of_five_questions(self):
        """
        Only 5 questions will be published on the main page
        """
        for i in range(10):
            create_question("Sample Question", -30)

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.context['latest_questions'].count(), 5)
