class ControlAgent:
    """
    Simple rule-based controller mimicking RL behavior
    for demonstration. This is a placeholder
    """

    def get_action(self, state):
        T = state["T"]
        C = state["C"]

        action = {}

        # Maintain target conditions
        action["coolant_flow"] = 0.2 if T > 360 else 0.7
        action["feed_rate"] = 0.8 if C < 0.8 else 0.3

        return action

