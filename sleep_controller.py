class SleepController:
    def __init__(self, logging, config):
        self.logging = logging
        self.backoff = self.backoff_start = config.backoff_start
        self.backoff_stop = config.backoff_stop
        self.backoff_multipel = config.backoff_multipel

    def current_backoff(self) -> int:
        self.logging.debug('-- backoff ' + str(self.backoff))
        current_backoff = self.backoff
        self.backoff *= self.backoff_multipel
        self.backoff = self.backoff_stop if self.backoff > self.backoff_stop else self.backoff
        return current_backoff

    def reset(self) -> None:
        self.backoff = self.backoff_start
