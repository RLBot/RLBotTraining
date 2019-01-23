from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

class BrickBot(BaseAgent):
    """
    A bot which just sits there and wiggles its wheels
    as if it were as dumb as a brick.
    """

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        seconds = game_tick_packet.game_info.seconds_elapsed
        controller_state = SimpleControllerState()
        controller_state.steer = -1 if seconds % 1.0 < 0.5 else 1
        controller_state.handbrake = 1
        return controller_state
