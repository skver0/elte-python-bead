class EventAnalyzer:
    def get_joiners_multiple_meetings_method(self, events):
        joiners = {}
        for event in events:
            if event["joiners"]:
                for joiner in event["joiners"]:
                    if joiner["email"] in joiners:
                        joiners[joiner["email"]] += 1
                    else:
                        joiners[joiner["email"]] = 1

        return [ joiner for joiner in joiners if joiners[joiner] > 1 ]