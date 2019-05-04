from queue import Empty

from rlbot.agents.base_agent import SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.matchcomms.common_uses.set_attributes_message import handle_set_attributes_message
from rlbot.matchcomms.common_uses.reply import reply_to

from rlbottraining.example_bots.simple_bot.simple_bot import SimpleBot




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

            if handle_set_attributes_message(msg, self, allowed_keys=['steering_coefficient']):
                reply_to(self.matchcomms, msg)  # Let the sender know we've set the attribute.
            else:
                # Ignore messages that are not for us.
                self.logger.debug(f'Unhandled message: {msg}')


        # Business as usual - this reads from self.steering_coefficient
        # Note: This get_outout() call will not see the messages drained from self.matchcomms.incoming_broadcast above.
        return super().get_output(game_tick_packet)
