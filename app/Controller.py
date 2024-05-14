# Initialises the display values for a given polls vote percentage bar
def bar_init(poll):
        bar = {}
        bar["left"] = "width:" + str(poll.left_percentage()) + "%"
        bar["right"] = "width:" + str(poll.right_percentage()) + "%"
        bar["divider"] = "left:" + str(poll.left_percentage() - 0.5) + "%"
        if poll.left_percentage() == 0 or poll.left_percentage() == 100:
                bar["ShowDivider"] = False
        else:
                bar["ShowDivider"] = True
        return bar