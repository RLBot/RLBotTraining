from queue import Empty

from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from rlbottraining.example_bots.simple_bot import SimpleBot




class TweakedBot(SimpleBot):
    """
    A version of SimpleBot that accepts parameters over matchcomms.
    """

    def get_output(self, game_tick_packet: GameTickPacket) -> SimpleControllerState:
        for i in range(100):  # process at most 100 messages per tick.
            try:
                msg = self.matchcomms.incoming_broadcast.get_nowait()
            except Empty:
                break

            # Ignore messages that are not for us.
            # Note: We assume SimpleBot.get_output() does not try to read messages.
            if not msg.get('is_example_tweak_msg', None):
                continue
            if msg.get('target_player_index', None) != self.index:
                continue

            tweaks = msg.get('tweaks', {})
            # We're making an assumption that our base class has this attribute that we're tweaking.
            assert hassattr(self, 'steering_coefficient')
            if 'steering_coefficient' in tweaks:
                self.steering_coefficient = tweaks['steering_coefficient']
            else:
                self.logger.warning(f'Received a example_tweak_msg but it seemed empty. Here\'s the message: {msg}')

        # Business as usual - this reads from self.steering_coefficient
        return super().get_output(game_tick_packet)
