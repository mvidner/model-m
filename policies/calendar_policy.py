
def calendar_policy(graph, policy_coefs, history, tseries, time, contact_history=None):

    if int(time) == 11:
        # close everything
        close = ["nursary children",
                 "nursary teachers to children",
                 "lower elementary children",
                 "lower elementary teachers to children",
                 "higher elementary children",
                 "higher elementary teachers to children",
                 "highschool children",
                 "highschool teachers to children"
                 ]
        weaken = [
            "friend and relative encounetr",
            "work contacts",
            "workers to clients",
            "contacts of customers at shops",
            "public transport contacts"
        ]
        coefs = [0.1, 0.5, 0.5, 0.4, 0.3]
        graph.close_layers(close)
        graph.close_layers(weaken, coefs)
        return {"graph": None}

    if int(time) == 25:
        # open little bit
        stronger = [
            "friend and relative encounetr",
            "work contacts",
            "workers to clients",
            "contacts of customers at shops",
            "public transport contacts"
        ]
        coefs = [0.2, 0.75, 0.75, 0.5, 0.4]
        graph.close_layers(stronger, coefs)
        return {"graph": None}

    return {}
