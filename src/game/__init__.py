"""
Provide a Game class which store all the game's state.
"""

import threading


class Game:
    """Store game's states."""

    def __init__(self, config, view_cls, controller_cls, audio_player_cls):
        self.config = config
        self.running = False

        self.view_thread = None
        self.controller_thread = None
        self.audio_player_thread = None

        self.view = view_cls(self, **config.get('view', {}))
        self.controller = controller_cls(self, **config.get('controller', {}))
        self.audio_player = audio_player_cls(
            self, **config.get('audio_player', {}))

    def run(self):
        """Start the game."""

        if not self.running:
            self.view_thread = threading.Thread(target=self.view.run)
            self.controller_thread = threading.Thread(
                target=self.controller.run)
            self.audio_player_thread = threading.Thread(
                target=self.audio_player.run)

            self.view_thread.start()
            self.controller_thread.start()
            self.audio_player_thread.start()

            self.running = True

    def stop(self):
        """Stop the game."""

        if self.running \
                and self.view_thread is not None \
                and self.controller_thread is not None \
                and self.audio_player_thread is not None:
            self.view.stop()
            self.controller.stop()
            self.audio_player.stop()

            self.view_thread.join()
            self.controller_thread.join()
            self.audio_player_thread.join()

            self.running = False
