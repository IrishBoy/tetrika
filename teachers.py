import numpy as np
import pandas as pd
import datetime as dt 


pd.set_option('display.max_columns', 500)
with open("lessons.txt", "r") as lessonsFile:
    lessons = pd.DataFrame(np.genfromtxt(lessonsFile, skip_header=2, skip_footer=3, delimiter='|', dtype=str), dtype=None, columns=['id', 'event_id', 'subject', 'scheduled_time'])
    lessons['scheduled_time'] = pd.to_datetime(lessons['scheduled_time'])
    # lessons['scheduled_time'] = lessons['scheduled_time'].dt.date
    lessons.event_id = lessons.event_id.astype('int32')
    lessons = lessons.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    lessons.drop_duplicates(inplace=True)
with open("participants.txt", "r") as partFile:
    participants = pd.DataFrame(np.genfromtxt(partFile, skip_header=2, skip_footer=3, delimiter='|', dtype=str), dtype=None, columns=['event_id', 'user_id'])
    participants.event_id = participants.event_id.astype('int32')
    participants = participants.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    participants.drop_duplicates(inplace=True)
with open("quality.txt", "r") as qualFile:
    quality = pd.DataFrame(np.genfromtxt(qualFile, skip_header=2, skip_footer=3, delimiter='|', dtype=str), dtype=None, columns=['lesson_id', 'tech_quality'])
    quality.loc[quality['tech_quality'] == '', 'tech_quality'] = np.nan
    quality.tech_quality = quality.tech_quality.astype('float')
    quality = quality.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
with open("users.txt", "r") as userFile:
    users = pd.DataFrame(np.genfromtxt(userFile, skip_header=2, skip_footer=3, delimiter='|', dtype=str), dtype=None, columns=['id', 'role'])
    users = users.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    users.drop_duplicates(inplace=True)

phys_lessons = lessons[lessons['subject'] == 'phys']
teachers = users[users['role'] == 'tutor']
les_marks = pd.merge(phys_lessons, quality, left_on =['id'], right_on=['lesson_id'], how='inner').drop(['id'], axis=1)
mean_marks = les_marks.groupby(['lesson_id', 'scheduled_time', 'event_id'])['tech_quality'].mean().reset_index()
only_teachers = pd.merge(participants, teachers, left_on=['user_id'], right_on=['id'], how='inner').drop(['id'], axis=1)
full = pd.merge(mean_marks, only_teachers, on='event_id', how='inner')
full['date'] = full['scheduled_time'].dt.date
full.drop(['scheduled_time', 'role', 'lesson_id'], axis=1, inplace=True)
av_per_day = full.groupby(['date', 'user_id'])['tech_quality'].mean().reset_index()
print(av_per_day.loc[av_per_day.groupby('date')['tech_quality'].idxmin()])
