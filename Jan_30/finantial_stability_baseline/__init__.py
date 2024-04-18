from otree.api import *
import random
import numpy as np


class Subsession(BaseSubsession):
    pass

class C(BaseConstants):
    NAME_IN_URL = 'fs_baseline'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 2

class Player(BasePlayer):
    option = models.BooleanField(
        choices=[(True, 'Option C'), (False, 'Option D'),]
    )
    type = models.StringField()
    no = models.FloatField()
    sigval = models.FloatField()
    signal = models.FloatField()
    upper = models.FloatField()
    lower = models.FloatField()
    payoff_lower = models.FloatField()
    payoff_upper = models.FloatField()
    payoff_lower_50 = models.FloatField()
    payoff_upper_50 = models.FloatField()
    pay_round = models.FloatField(
        min=0,
        max=160,
    )
    portfolio = models.IntegerField(
        min=0,
        max=10,
    )



class Group(BaseGroup):
    portfolio = models.IntegerField(
        min=0,
        max=10,
    )
    rn = models.IntegerField(
        min=-5,
        max=20,
    )
    assetvalue = models.FloatField()
    seconds = models.IntegerField(
        min=0,
        max=2,
    )

def creating_session(s):
    # assign types to players
    for p in s.get_players():
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

    print('round' + str(s.round_number) + 'modified group matrix')

    for g in s.get_groups():
        g.rn = g.round_number
        g.assetvalue = round(np.random.uniform(90, 160), 3)
        for p in g.get_players():
            p.no = round(np.random.uniform(0,20) - 10, 3)
            p.sigval = g.assetvalue + p.no
            if p.sigval >= 160:
                p.signal = 160
            elif p.sigval <= 90:
                p.signal = 90
            elif p.sigval <= 160 and p.sigval >= 90:
                p.signal = p.sigval
            if p.signal >= 150:
                p.upper = 160
            else:
                p.upper = p.signal + 10
            if p.signal <= 100:
                p.lower = 90
            else:
                p.lower = p.signal - 10

def portfolio_choice(g: Group):
    return g.portfolio

def setPayoffs(g: Group):
    g.seconds = 0
    for p in g.get_players():
        p.portfolio = g.portfolio
        if p.option == True and p.type == 'second_mover':
            g.seconds += 1
    for p in g.get_players():
        if p.type == 'second_mover' and p.option == True and g.seconds == 2:
            p.pay_round = (g.portfolio/10)*g.assetvalue + ((10-g.portfolio)/10)*125
        elif p.type == 'second_mover' and p.option == True and g.seconds == 1:
            p.pay_round = (g.portfolio/10)*g.assetvalue + ((10-g.portfolio)/10)*125 - 50
        elif p.type == 'second_mover' and p.option == False:
            p.pay_round = 100
        elif p.type == 'first_mover' and g.seconds == 2:
            p.pay_round = (g.portfolio/10)*g.assetvalue + ((10-g.portfolio)/10)*125
        elif p.type == 'first_mover' and g.seconds == 1:
            p.pay_round = ((g.portfolio/10)*g.assetvalue + ((10-g.portfolio)/10)*125 - 50 + 100)/2
        elif p.type == 'first_mover' and g.seconds == 0:
            p.pay_round = 100

#class Intro(Page):
    #@staticmethod
    #def is_displayed(player):
    #    return player.round_number == 1

#class PracticeFirst(Page):
#    form_model = 'group'
#    form_fields = ['portfolio']
#    @staticmethod
#    def is_displayed(player):
#        return player.id_in_group == 1 and player.round_number >= 2 and player.round_number <= 6

#class PracticeSecond(Page):
#    form_model = 'player'
#    form_fields = ['option']
#    @staticmethod
#    def is_displayed(player):
#        return player.id_in_group != 1 and player.round_number >= 2 and player.round_number <= 6

class First(Page):
    form_model = 'group'
    form_fields = ['portfolio']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group == 1
    @staticmethod
    def vars_for_template(player):
        if player.type == 'first_mover':
            player.option = False
        return dict(
            option = player.option,
        )
class Second(Page):
    form_model = 'player'
    form_fields = ['option']
    @staticmethod
    def is_displayed(player):
        return player.id_in_group != 1
    @staticmethod
    def vars_for_template(p: Player):
        g = p.group
        p.payoff_upper = round((g.portfolio / 10) * p.upper + ((10 - g.portfolio) / 10) * 125, 3)
        p.payoff_lower = round((g.portfolio / 10) * p.lower + ((10 - g.portfolio) / 10) * 125, 3)
        p.payoff_upper_50 = p.payoff_upper - 50
        p.payoff_lower_50 = p.payoff_lower - 50
        return dict(
            payoff_upper=p.payoff_upper,
            payoff_lower=p.payoff_lower,
            payoff_upper_50=p.payoff_upper_50,
            payoff_lower_50=p.payoff_lower_50,
        )

class WaitFromIntro(WaitPage):
    wait_for_all_groups = True
    body_text = 'Waiting for others to read the introduction'
    after_all_players_arrive = 'creating_session'
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
class WaitForP1(WaitPage):
    body_text = "Waiting for the choice of the first mover"

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'setPayoffs'
    body_text = 'Waiting for the second movers choices'

class Results(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.round_number == C.NUM_ROUNDS:
                random_round = random.randint(1, C.NUM_ROUNDS)
                print(random_round)
                player_in_selected_round = player.in_round(random_round)
                player.payoff = player_in_selected_round.pay_round

class RegroupWaitPage(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting for random regrouping with other two players"
    after_all_players_arrive = 'creating_session'
    @staticmethod
    def is_displayed(player):
        return player.round_number < C.NUM_ROUNDS

class FinalWaitPage(WaitPage):
    wait_for_all_groups = True
    body_text = "Waiting for others finishing the games"
    after_all_players_arrive = 'creating_session'
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

class FinalResults(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

page_sequence = [WaitFromIntro, First, WaitForP1, Second, ResultsWaitPage, Results, RegroupWaitPage, FinalWaitPage, FinalResults]
