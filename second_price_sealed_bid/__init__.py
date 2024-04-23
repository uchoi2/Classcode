from otree.api import *
import random


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'second_price_auction'
    players_per_group = 3
    num_rounds = 10
    # timeout_seconds = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    second_highest_bid = models.CurrencyField()
    winner = models.IntegerField()
    price = models.CurrencyField()


class Player(BasePlayer):
    value = models.CurrencyField()
    bid = models.CurrencyField(initial=0)
    is_winner = models.BooleanField()
    # price = models.CurrencyField()


# FUNCTIONS


def creating_session(subsession):
    if subsession.round_number == 1 or subsession.round_number == 6:
        subsession.group_randomly()
    else:
        subsession.group_like_round(subsession.round_number - 1)

    for p in subsession.get_players():
        p.value = random.random()*100
        p.is_winner = False
        if subsession.round_number == 1:
            p.participant.vars['totalEarnings'] = 0
            p.participant.vars['finished'] = False


def auction_outcome(g: Group):

    # Get the set of players in the group
    players = g.get_players()

    # Get the set of bids from the players
    bids = [p.bid for p in players if p.bid >= 0]

    # Sort the bids in descending order
    bids.sort(reverse=True)

    # Set the highest and second-highest bids to the appropriate group variables
    # (Python uses 0-based arrays...)
    g.highest_bid = bids[0]
    g.second_highest_bid = bids[1]

    # Tiebreak
    # We always do this even when there is not a tie...
    ###########
    # first get the set of player IDs who bid the highest
    highest_bidders = [p.id_in_group for p in players if p.bid == g.highest_bid]

    # next randomly select one of these player IDs  to be the winner
    g.winner = random.choice(highest_bidders)

    # finally get the player model of the winning bidder and flag as winner
    winning_player = g.get_player_by_id(g.winner)
    winning_player.is_winner = True

    # Set payoffs
    #############
    for p in players:
        if p.is_winner:
            p.payoff = p.value - g.second_highest_bid
            p.participant.vars['finished'] = True
        else:
            p.payoff = 0
    g.price = g.second_highest_bid


# PAGES
class bid(Page):
    # def is_displayed(player):
    #     return player.participant.vars['finished']

    form_model = 'player'
    form_fields = ['bid']

    # def get_timeout_seconds(player):
    #     return Constants.timeout_seconds  # in seconds
    #
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     if timeout_happened:
    #         player.bid = random.random()*player.value


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'auction_outcome'
    body_text = "Please wait for everyone to submit bids."


class Results(Page):
    pass
    # @staticmethod
    # def get_timeout_seconds(player):
    #     return Constants.timeout_seconds

    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     if timeout_happened:
    #         player.bid = c(9.89)


page_sequence = [bid, ResultsWaitPage, Results]