class MissionError(Exception):
    pass


class InvalidTransitionError(MissionError):
    pass


class SessionNotFoundError(MissionError):
    pass


class LearnerMismatchError(MissionError):
    pass


class InvalidDecisionError(MissionError):
    pass


class StageProgressionError(MissionError):
    pass
