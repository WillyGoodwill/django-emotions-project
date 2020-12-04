import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'emotions_project.settings')
import django
django.setup()

import random
from basic_app.models import MoodTracker
from faker import Faker

fakegen = Faker()



def populate(N=5):
    for entry in range(N):
        fake_date =fakegen.date()
        mood_db = MoodTracker.objects.get_or_create(mood = random.choice(range(10)),
                                                    datetime = fake_date)[0]

if __name__ == '__main__':
    print('populating')
    populate(20)