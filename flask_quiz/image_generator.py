import os
from wordcloud import WordCloud

from flask_quiz import app
from flask_quiz.database import get_all_answers


def generate_wordcloud_img():
    words = [a.text for a in get_all_answers()]
    print(words)
    is_wordcloud_generated = False
    if len(words) > 0:
        try:
            wordcloud = WordCloud(width=1024, height=1024, margin=0).generate(' '.join(words))
            wordcloud.to_file('{}/wordcloud.png'.format(os.path.join(app.config['IMAGE_FOLDER'])))
            is_wordcloud_generated = True
        except ValueError:
            is_wordcloud_generated = False
    return is_wordcloud_generated
