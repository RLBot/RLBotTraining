from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

class PropBot(BaseAgent):
    """
    A bot which just sits there like a prop.
    """

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        seconds = game_tick_packet.game_info.seconds_elapsed
        controller_state = SimpleControllerState()
        controller_state.steer = 0
        controller_state.handbrake = 0
        return controller_state
