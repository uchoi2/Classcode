from otree.api import *

#Define basic subsession
class Subsession(BaseSubsession):
    pass

#Define basic constant
class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 4
    ENDOWMENT = cu(1000)
    # Other way to define multiple MPCR
    MPCR_1 = 0.4
    MPCR_2 = 0.6


#Define Model : Record data point we need
class Player(BasePlayer):                       # Individual Action Class
    contribution = models.CurrencyField(        # define value contribution (multiple players)
        min=0,                                  # Minimum contribution
        max=C.ENDOWMENT,                        # Maximum contribution
        label="How much will you contribute?"   # Text displayed on the player's screen
    )

class Group(BaseGroup):                         # Group Action define
    mpcr = models.FloatField(initial=0)
    total_contribution= models.CurrencyField()  # Total Contribution
    individual_share= models.CurrencyField()    # Individual Share

#Define pages
#Page 1, Contribute
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

#Page 2, Results wait
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'setPayoffs'
    body_text = 'You are too fast! Slow Down!'

#Page 3, Results page
class Results(Page):
    pass

page_sequence = [Contribute, ResultsWaitPage, Results]


# Functions
def creating_session(subsession):
    print('In creating sessions') #debug server side error

    # establish a total earnings variable for each participant and initialize to 0 at beginning of session.

    for p in subsession.get_players():
        if subsession.round_number == 1:
            p.participant.vars['totalEarnings'] = 0

    # Assign varying MPCR (First half of periods one value and second half the other)

    for g in subsession.get_groups():
        print('round', subsession.round_number)
        print('num_rounds/2', int(C.NUM_ROUNDS/2))
        if subsession.round_number <= int(C.NUM_ROUNDS/2):      # In first half...
            g.mpcr = C.MPCR_1
        else:
            g.mpcr = C.MPCR_2
        print('MPCR: ', g.mpcr)

def setPayoffs(g: Group):           #set_payoffs = setPayoffs
    # calculate total group contribution
    g.total_contribution = 0
    for p in g.get_players():
        g.total_contribution += p.contribution

    # calculate individual earnings
    for p in g.get_players():
        p.participant.payoff = C.ENDOWMENT \
                               - p.contribution \
                               + g.mpcr*g.total_contribution/C.PLAYERS_PER_GROUP
        p.participant.vars['totalEarnings'] += p.participant.payoff

    # I need to check this precisely uploaded at the Github Errorchecking