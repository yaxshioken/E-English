from django.db.models import TextChoices


class OptionTest(TextChoices):
    A = 'a', "A"
    B = 'b', "B"
    C = 'c', "C"
    D = 'd', "D"


class ResultType(TextChoices):
        TEST = 'test' , 'Test'
        TEXT = 'text' , 'Text'
        AUDIO = 'audio' , 'Audio'
        LISTENING = 'listening' , 'Listening'
        WRITING = 'writing' , 'Writing'
        READING = 'reading' , 'Reading'
        SPEAKING = 'speaking' , 'Speaking'