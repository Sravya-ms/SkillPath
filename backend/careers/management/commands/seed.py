from django.core.management.base import BaseCommand
from django.utils.text import slugify
from careers.catalog import ROLES, NON_DEV, NO_GIT, WEB_SKILLS
from careers.topics import TOPIC_DEFS
from careers.models import CareerPath, CareerSkill
from learning.models import Topic, ExamQuestion

# skill -> list of (question, options, index of correct option)
QUESTIONS = {
    'html': [
        ('Which tag holds the main navigation links semantically?', ['<nav>', '<div>', '<span>', '<section>'], 0),
        ('Which attribute gives an image text for screen readers?', ['alt', 'src', 'title', 'href'], 0),
        ('Which element is used for the largest heading?', ['<h1>', '<head>', '<header>', '<title>'], 0),
        ('What does the <form> action attribute define?', ['Where data is sent', 'Form color', 'Input type', 'Page title'], 0)],
    'css': [
        ('Which property enables Flexbox on a container?', ['display: flex', 'flex: on', 'position: flex', 'align: flex'], 0),
        ('In the box model, what sits between content and border?', ['padding', 'margin', 'outline', 'gap'], 0),
        ('Which unit is relative to the viewport width?', ['vw', 'px', 'pt', 'cm'], 0),
        ('Which at-rule makes responsive breakpoints?', ['@media', '@import', '@font-face', '@keyframes'], 0)],
    'javascript': [
        ('Which keyword declares a block-scoped variable you can reassign?', ['let', 'const', 'var only', 'static'], 0),
        ('What does === check?', ['Value and type equality', 'Value only', 'Assignment', 'Reference only for numbers'], 0),
        ('Which method adds an item to the end of an array?', ['push', 'pop', 'shift', 'slice'], 0),
        ('What does async/await help with?', ['Writing asynchronous code readably', 'Styling', 'Loops only', 'Type checking'], 0)],
    'git': [
        ('Which command records staged changes?', ['git commit', 'git push', 'git clone', 'git fetch'], 0),
        ('Which command creates a new branch and switches to it?', ['git checkout -b name', 'git branch -d name', 'git merge name', 'git stash'], 0),
        ('What is a pull request for?', ['Proposing and reviewing changes before merging', 'Deleting a repo', 'Downloading code', 'Reverting a commit'], 0),
        ('Which command downloads a remote repo?', ['git clone', 'git init', 'git add', 'git log'], 0)],
}


class Command(BaseCommand):
    help = 'Seed careers, roadmap topics and a starter question bank (safe to re-run).'

    ORDER = {'prompt engineering': 3, 'llm': 4, 'rag': 6, 'vector database': 6, 'langchain': 6, 'openai api': 5,
             'ai agents': 8, 'mlops': 8, 'mlflow': 7, 'kafka': 6, 'dbt': 5, 'snowflake': 6, 'data modeling': 4,
             'scrum': 3, 'kanban': 4, 'product management': 3, 'roadmapping': 5, 'project management': 3,
             'ms project': 5, 'troubleshooting': 1, 'bash': 2, 'windows server': 3, 'powershell': 4,
             'active directory': 5, 'iam': 5, 'cisco': 4, 'prometheus': 6, 'grafana': 7, 'owasp': 4,
             'pentesting': 5, 'burp suite': 6, 'siem': 4, 'incident response': 6, 'forensics': 5,
             'seo': 3, 'content marketing': 4, 'keyword research': 4, 'google analytics': 4, 'a/b testing': 6}

    def handle(self, *a, **kw):
        paths = {}
        for r in ROLES:
            c, _ = CareerPath.objects.get_or_create(slug=slugify(r['title']),
                                                    defaults={'title': r['title'], 'description': r['desc']})
            if not c.skills.exists():
                CareerSkill.objects.bulk_create([CareerSkill(career=c, skill=k, weight=w) for k, w in r['skills'].items()])
            paths[r['title']] = (c, r)
        for order, title, skill, desc in TOPIC_DEFS:
            Topic.objects.get_or_create(title=title, defaults={'order': order, 'skill': skill, 'description': desc})
        # every skill used by a role gets a topic (hand-written one if present, else generated)
        by_skill = {t.skill: t for t in Topic.objects.exclude(skill='')}
        for skill in sorted({k for r in ROLES for k in r['skills']}):
            if skill not in by_skill:
                title = skill.upper() if len(skill) <= 4 else skill.title()
                t, _ = Topic.objects.get_or_create(title=title, defaults={
                    'skill': skill, 'order': self.ORDER.get(skill, 5),
                    'description': f'Core concepts of {title}, hands-on practice, then one small project.'})
                by_skill[skill] = t
        web, git = Topic.objects.get(title='Web basics'), Topic.objects.get(title='Git and GitHub')
        proj, intv = Topic.objects.get(title='Projects'), Topic.objects.get(title='Interview preparation')
        for c, r in paths.values():
            for skill in r['skills']:
                by_skill[skill].careers.add(c)
            proj.careers.add(c)
            intv.careers.add(c)
            if WEB_SKILLS & set(r['skills']):
                web.careers.add(c)
            if r['category'] not in NON_DEV and r['title'] not in NO_GIT:
                git.careers.add(c)
        for skill, qs in QUESTIONS.items():
            t = Topic.objects.get(skill=skill)
            if not t.questions.exists():
                ExamQuestion.objects.bulk_create([ExamQuestion(topic=t, text=q, options=o, correct=i) for q, o, i in qs])
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(paths)} roles and {Topic.objects.count()} topics. Add exam questions in /admin (aim for 15+ per topic).'))
