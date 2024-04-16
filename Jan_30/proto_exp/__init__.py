from otree.api import *
import random
import numpy as np


class Subsession(BaseSubsession):
    pass

class C(BaseConstants):
    NAME_IN_URL = 'Financial_Stability'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 27

class Player(BasePlayer):
    portfolio = models.IntegerField(
        min=0,
        max=10
    )
    option = models.BooleanField(
        choices=[(True, 'Option C'), (False, 'Option D'),]
    )

class Group(BaseGroup):
    pass


def creating_session(s):
    # assign types to players
    for p in s.get.players():
        if p.id_in_group == 1:
            p.type = 'first_mover'
        else:
            p.type = 'second_mover'
    # randomly shuffle all second movers
    print("-------------------------------")
    print('round' + str(s.round_number) + 'default group matrix')
    m = s.get_group_matrix()
    print(m)

    ungrouped_second_mover = []

    for row in m:
        ungrouped_second_mover.append(row[1])
        ungrouped_second_mover.append(row[2])

    print('ungrouped_second_mover: ',  ungrouped_second_mover)

    new_m = []
    print('new_group_matrix: ', new_m)

    for row in m:
        p1 = row[0]
        p2 = ungrouped_second_mover.pop(random.randrange(len(ungrouped_second_mover)))
        print('ungrouped_second_mover: ', ungrouped_second_mover)
        p3 = ungrouped_second_mover.pop(random.randrange(len(ungrouped_second_mover)))
        print('ungrouped_second_mover: ', ungrouped_second_mover)

        new_m.append([p1, p2, p3])
        print('new_group_matrix: ', new_m)

    s.set_group_matrix(new_m)

    print('round' + str(s.NUM_ROUNDS) + 'modified group matrix')

def setPayoffs(g: Group):
    # Set up the baseline info
    g.assetdraw = np.random.uniform(90, 160)
    g.assetvalue = round(g.assetdraw, 3)

    g.seconds = 0
    for p in g.get_players():
        p.no = np.random.uniform(0,20)
        p.noise = p.no - 10
        p.signal = g.assetvalue + round(p.noise, 3)
        g.first = p.portfolio
        if p.option == 'option C':
            g.seconds += 1
        p.paylist = []
        if p.type == 'second_mover' and p.option == 'option C' and g.seconds == 2:
            p.payoff = (g.first/10)*g.assetvalue + ((10-g.first)/10)*125
            p.paylist.append(p.payoff)
        elif p.type == 'second_mover' and p.option == 'option C' and g.seconds == 1:
            p.payoff = (g.first/10)*g.assetvalue + ((10-g.first)/10)*125 - 50
            p.paylist.append(p.payoff)
        elif p.type == 'second_mover' and p.option == 'option D':
            p.payoff = 100
            p.paylist.append(p.payoff)
        elif p.type == 'first_mover' and g.seconds == 2:
            p.payoff = (g.first/10)*g.assetvalue + ((10-g.first)/10)*125
            p.paylist.append(p.payoff)
        elif p.type == 'first_mover' and g.seconds == 1:
            p.payoff = (g.first/10)*g.assetvalue + ((10-g.first)/10)*125 - 25
            p.paylist.append(p.payoff)
        elif p.type == 'first_mover' and g.seconds == 0:
            p.payoff = 100
            p.paylist.append(p.payoff)
        p.final = p.random.choice(p.paylist)

class Intro(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

class PracticeFirst(Page):
    form_model = 'player'
    form_fields = ['portfolio']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1 and player.round_number >= 2 and player.round_number <= 6

class PracticeSecond(Page):
    form_model = 'player'
    form_fields = ['option']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group != 1 and player.round_number >= 2 and player.round_number <= 6

class First(Page):
    form_model = 'player'
    form_fields = ['portfolio']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1 and player.round_number >= 7 and player.round_number <= 26
class Second(Page):
    form_model = 'player'
    form_fields = ['option']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group != 1 and player.round_number >= 7 and player.round_number <= 26

class WaitForP1(WaitPage):
    body_text = "Waiting for the choice of the first mover"
    @staticmethod
    def is_displayed(player):
        return player.round_number >= 2

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'setPayoffs'
    body_text = 'Waiting for the second movers choices'
    @staticmethod
    def is_displayed(player):
        return player.round_number >= 2

class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number >= 2
class FinalResults(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 27

page_sequence = [Intro, PracticeFirst, First, WaitForP1, PracticeSecond, Second, ResultsWaitPage, Results, FinalResults]


