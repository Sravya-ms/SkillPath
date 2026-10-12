import io

import docx
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from resumes.models import ResumeVersion


def make_docx(text):
    d = docx.Document()
    d.add_paragraph(text)
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


class UploadTests(TestCase):
    def setUp(self):
        User.objects.create_user('a', password='pw12345!x')
        self.client.login(username='a', password='pw12345!x')

    def test_docx_upload_is_stored_in_database_and_versions_are_separate(self):
        data = make_docx('Skills: Python, Django, HTML, CSS, JavaScript, Git, SQL')
        for _ in range(2):  # same file name twice -> two versions
            r = self.client.post('/resumes/upload/', {'resume': SimpleUploadedFile('cv.docx', data)})
            self.assertEqual(r.status_code, 302)
        self.assertEqual(ResumeVersion.objects.count(), 2)
        rv = ResumeVersion.objects.first()
        self.assertEqual(rv.status, 'complete')
        self.assertTrue(len(rv.skills) >= 4)
        self.assertEqual(bytes(rv.file_data), data)

    def test_oversized_file_rejected(self):
        big = SimpleUploadedFile('big.pdf', b'%PDF' + b'0' * (4 * 1024 * 1024 + 1))
        self.client.post('/resumes/upload/', {'resume': big})
        self.assertEqual(ResumeVersion.objects.count(), 0)
