from otree.api import *
import random

#Define basic constant
class C(BaseConstants):
    NAME_IN_URL = '2nd_Price_Sealed_Bid'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    highest_bid = models.CurrencyField()
    second_highest_bid = models.CurrencyField()
    winning_player = models.IntegerField()

class Player(BasePlayer):
    bid = models.CurrencyField(initial=0)
    value = models.CurrencyField()
    win = models.BooleanField(initial=False)             #Binary Variable Field
    price = models.CurrencyField()

#Functions
def creating_session(subsession):
    for p in subsession.get_players():
        p.value = random.random()*100
        #p.is_winner = False
        if subsession.round_number == 1:    #Only if at the beginning of the fist sessions.
            p.participant.vars['totalEarnings'] = 0
            #p.participant.vars['finished'] = False

def auction_outcome(g: Group):

    # Get the set of players in the group
    players = g.get_players()

    # Get the set of bids from the players
    #bids = [p.bid for p in players if p.bid >= 0]
    bids = [p.bid for p in players]

    # Sort the bids in descending order
    bids.sort(reverse=True)

    # Set the highest and second-highest bids to the appropriate group variables
    g.highest_bid = bids[0]
    g.second_highest_bid = bids[1]

    # Tiebreak
    # Random Choice between the highest bidders
    highest_bidders = [p.id_in_group for p in players if p.bid == g.highest_bid]
    g.winning_player = random.choice(highest_bidders)

    # Finally get the player model of the winning bidder and flag as winner
    winning_player = g.get_player_by_id(g.winning_player)
    winning_player.win = True

    # Set payoffs
    for p in players:
        if p.win:
            p.payoff = p.value - g.second_highest_bid
            #p.participant.vars['finished'] = True
        else:
            p.payoff = 0
        p.price = g.highest_bid
# Define Pages

#Page 1, Bidding Page
class bid(Page):
    form_model = 'player'
    form_fields = ['bid']

#Page 2, Results wait
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'auction_outcome'

#Page 3, Results pape
class Results(Page):
    pass

page_sequence = [bid, ResultsWaitPage, Results]