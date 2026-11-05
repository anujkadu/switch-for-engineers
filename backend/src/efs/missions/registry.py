from efs.missions.definitions import MissionDefinition


class MissionNotFoundError(LookupError):
    pass


class MissionRegistry:
    def __init__(self, definitions: tuple[MissionDefinition, ...] = ()) -> None:
        self._definitions = {(item.mission_id, item.version): item for item in definitions}

    def get(self, mission_id: str, version: str) -> MissionDefinition:
        try:
            return self._definitions[(mission_id, version)]
        except KeyError as exc:
            raise MissionNotFoundError(
                f"unknown mission {mission_id!r} version {version!r}"
            ) from exc
