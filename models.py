from dataclasses import dataclass


@dataclass(frozen=True)
class Teacher:
    id: int | None
    name: str
    active: bool = True


@dataclass(frozen=True)
class TeacherAvailability:
    id: int | None
    teacher_id: int
    weekday: int
    start_time: str
    end_time: str


@dataclass(frozen=True)
class Studio:
    id: int | None
    name: str
    active: bool = True


@dataclass(frozen=True)
class DanceClass:
    id: int | None
    name: str
    style: str
    age_group: str
    duration_minutes: int
    preferred_teacher_id: int | None = None
    active: bool = True


@dataclass(frozen=True)
class ScheduleEntry:
    id: int | None
    class_id: int
    teacher_id: int
    studio_id: int
    weekday: int
    start_time: str
    end_time: str
