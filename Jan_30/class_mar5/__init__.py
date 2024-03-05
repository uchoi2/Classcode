from otree.api import *
import random

# Define Subsession
class Subsessions(BaseSubsession):
    pass

class C(BaseConstants):
    NAME_IN_URL = 'rock_paper_scissor'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
    ENDOWMENT = cu(1000)


class Player(BasePlayer):
    action = models.IntegerField(initial=0)
    payout = models.IntegerField()
    winning = models.BooleanField(initial=False)

class Group(BaseGroup):
    winning_players = models.IntegerField()

# Defining Functions
def creating_session(s: Subsessions):
    for p in s.get.players():
        if p.id_in_group % 2 == 0:
            p.type = 1
        else:
            p.type = 2
def outcome(g: Group):
    row_action = -999
    col_action = -999
    players = g.get_players()
    for p in players:
        if p.type == 1:
            row_action = p.action
        else:
            col_action = p.action
    if (row_action == 2 and col_action == 1) or (row_action == 3 and col_action == 2) or (row.action == 1 and col_action == 3):
        g.winning_players
# Define Pages
class Action(Page):
    form_model = 'player'
    form_fields = ['action']

class ResultsWaitingPage(WaitPage):
    pass

class Results(Page):
    pass