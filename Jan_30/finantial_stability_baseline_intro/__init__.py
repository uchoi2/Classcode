from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'fs_baseline_intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
# PAGES
class Intro(Page):
    pass


page_sequence = [Intro]
