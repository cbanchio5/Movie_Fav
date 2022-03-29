from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, StringField
from wtforms.validators import DataRequired, Length


class EditForm(FlaskForm):
    rating = FloatField(
        'New Rating',
        [DataRequired()]
    )

    review = StringField('New Review',
        [DataRequired()]
    )

    submit = SubmitField('Submit')


class AddForm(FlaskForm):
    movie_title = StringField(
        'New Title',
        [DataRequired()]
    )

    submit = SubmitField('Add')
