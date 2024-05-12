# Initialises the display values for a given polls vote percentage bar
def bar_init(poll):
        bar = {}
        bar["left"] = "width:" + str(poll["left%"]) + "%"
        bar["right"] = "width:" + str(poll["right%"]) + "%"
        bar["divider"] = "left:" + str(poll["left%"] - 0.5) + "%"
        return bar