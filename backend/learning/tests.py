from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from careers.models import CareerPath, CareerSkill
from careers.scoring import score_resume
from learning.models import Topic, ExamQuestion, ExamAttempt
from resumes.models import ResumeVersion


class ExamAndPrivacyTests(TestCase):
    def setUp(self):
        self.a = User.objects.create_user('a', password='pw12345!x')
        self.b = User.objects.create_user('b', password='pw12345!x')
        self.topic = Topic.objects.create(title='T', skill='html', order=1)
        for i in range(4):
            ExamQuestion.objects.create(topic=self.topic, text=f'q{i}', options=['r', 'x', 'y', 'z'], correct=0)

    def _take(self, wrong):
        self.client.get(f'/learning/exam/{self.topic.pk}/')
        ids = self.client.session[f'exam_{self.topic.pk}']
        data = {f'q{pk}': ('1' if n < wrong else '0') for n, pk in enumerate(ids)}
        return self.client.post(f'/learning/exam/{self.topic.pk}/', data)

    def test_75_percent_passes(self):
        self.client.login(username='a', password='pw12345!x')
        self._take(wrong=1)
        self.assertTrue(ExamAttempt.objects.get().passed)

    def test_50_percent_fails_and_attempts_count(self):
        self.client.login(username='a', password='pw12345!x')
        self._take(wrong=2)
        self._take(wrong=2)
        self.assertFalse(ExamAttempt.objects.filter(passed=True).exists())
        self.assertEqual(ExamAttempt.objects.latest('taken_at').attempt_no, 2)

    def test_other_user_cannot_open_resume(self):
        rv = ResumeVersion.objects.create(user=self.a, file=SimpleUploadedFile('r.pdf', b'%PDF-x'), file_name='r.pdf')
        self.client.login(username='b', password='pw12345!x')
        self.assertEqual(self.client.get(f'/resumes/{rv.pk}/review/').status_code, 404)
        self.assertEqual(self.client.get(f'/careers/results/{rv.pk}/').status_code, 404)

    def test_scores_sorted_descending(self):
        for n, skills in enumerate([['html'], ['html', 'css'], ['css', 'git']]):
            c = CareerPath.objects.create(title=f'C{n}', slug=f'c{n}')
            for s in skills:
                CareerSkill.objects.create(career=c, skill=s, weight=1)
        scores = [r['score'] for r in score_resume(['html', 'css'])]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_invalid_file_rejected(self):
        self.client.login(username='a', password='pw12345!x')
        self.client.post('/resumes/upload/', {'resume': SimpleUploadedFile('fake.pdf', b'not a pdf')})
        self.assertEqual(ResumeVersion.objects.count(), 0)
