import sqlite3
from pathlib import Path
from typing import Any


class Database:
    def __init__(self, database_path: str) -> None:
        self.database_path = Path(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    active INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS studios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    active INTEGER NOT NULL DEFAULT 1
                );

                CREATE TABLE IF NOT EXISTS dance_classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL COLLATE NOCASE,
                    style TEXT NOT NULL,
                    age_group TEXT,
                    duration_minutes INTEGER NOT NULL DEFAULT 60,
                    preferred_teacher_id INTEGER,
                    active INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (preferred_teacher_id)
                        REFERENCES teachers(id)
                        ON DELETE SET NULL
                );

                CREATE TABLE IF NOT EXISTS teacher_availability (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id INTEGER NOT NULL,
                    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    UNIQUE (teacher_id, weekday, start_time, end_time),
                    FOREIGN KEY (teacher_id)
                        REFERENCES teachers(id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS schedule_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_id INTEGER NOT NULL,
                    teacher_id INTEGER NOT NULL,
                    studio_id INTEGER NOT NULL,
                    weekday INTEGER NOT NULL CHECK (weekday BETWEEN 0 AND 6),
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    FOREIGN KEY (class_id)
                        REFERENCES dance_classes(id)
                        ON DELETE RESTRICT,
                    FOREIGN KEY (teacher_id)
                        REFERENCES teachers(id)
                        ON DELETE RESTRICT,
                    FOREIGN KEY (studio_id)
                        REFERENCES studios(id)
                        ON DELETE RESTRICT
                );

                CREATE INDEX IF NOT EXISTS idx_availability_teacher_day
                    ON teacher_availability (teacher_id, weekday);

                CREATE INDEX IF NOT EXISTS idx_schedule_teacher_day
                    ON schedule_entries (teacher_id, weekday);

                CREATE INDEX IF NOT EXISTS idx_schedule_studio_day
                    ON schedule_entries (studio_id, weekday);
                """
            )

    def add_teacher(self, name: str) -> int:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Teacher name cannot be blank.")

        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    "INSERT INTO teachers (name) VALUES (?)",
                    (normalized_name,),
                )
                return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"{normalized_name} is already in the teacher list."
            ) from exc

    def list_teachers(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name
                FROM teachers
                WHERE active = 1
                ORDER BY name
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def delete_teacher(self, teacher_id: int) -> None:
        try:
            with self._connect() as connection:
                connection.execute(
                    "DELETE FROM teachers WHERE id = ?",
                    (teacher_id,),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "This teacher is already assigned to the schedule. "
                "Remove their scheduled classes first."
            ) from exc

    def add_teacher_availability(
        self,
        teacher_id: int,
        weekday: int,
        start_time: str,
        end_time: str,
    ) -> int:
        if start_time >= end_time:
            raise ValueError(
                "The end time must be later than the start time."
            )

        with self._connect() as connection:
            overlap = connection.execute(
                """
                SELECT id
                FROM teacher_availability
                WHERE teacher_id = ?
                  AND weekday = ?
                  AND start_time < ?
                  AND end_time > ?
                LIMIT 1
                """,
                (teacher_id, weekday, end_time, start_time),
            ).fetchone()

            if overlap:
                raise ValueError(
                    "This availability overlaps an existing time "
                    "for that teacher."
                )

            try:
                cursor = connection.execute(
                    """
                    INSERT INTO teacher_availability (
                        teacher_id,
                        weekday,
                        start_time,
                        end_time
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (teacher_id, weekday, start_time, end_time),
                )
                return int(cursor.lastrowid)
            except sqlite3.IntegrityError as exc:
                raise ValueError(
                    "That exact availability is already saved."
                ) from exc

    def list_teacher_availability(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    teacher_availability.id,
                    teacher_availability.teacher_id,
                    teachers.name AS teacher_name,
                    teacher_availability.weekday,
                    teacher_availability.start_time,
                    teacher_availability.end_time
                FROM teacher_availability
                INNER JOIN teachers
                    ON teachers.id = teacher_availability.teacher_id
                ORDER BY
                    teachers.name,
                    teacher_availability.weekday,
                    teacher_availability.start_time
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def delete_teacher_availability(
        self,
        availability_id: int,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM teacher_availability WHERE id = ?",
                (availability_id,),
            )

    def add_studio(self, name: str) -> int:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Studio name cannot be blank.")

        try:
            with self._connect() as connection:
                cursor = connection.execute(
                    "INSERT INTO studios (name) VALUES (?)",
                    (normalized_name,),
                )
                return int(cursor.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                f"{normalized_name} is already in the studio list."
            ) from exc

    def list_studios(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name
                FROM studios
                WHERE active = 1
                ORDER BY name
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def delete_studio(self, studio_id: int) -> None:
        try:
            with self._connect() as connection:
                connection.execute(
                    "DELETE FROM studios WHERE id = ?",
                    (studio_id,),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "This studio is already used by the schedule. "
                "Remove its scheduled classes first."
            ) from exc

    def add_dance_class(
        self,
        name: str,
        style: str,
        age_group: str,
        duration_minutes: int,
        preferred_teacher_id: int | None,
    ) -> int:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Class name cannot be blank.")

        if duration_minutes <= 0:
            raise ValueError("Class duration must be greater than zero.")

        with self._connect() as connection:
            duplicate = connection.execute(
                """
                SELECT id
                FROM dance_classes
                WHERE name = ? COLLATE NOCASE
                  AND active = 1
                LIMIT 1
                """,
                (normalized_name,),
            ).fetchone()

            if duplicate:
                raise ValueError(
                    f"{normalized_name} is already in the class list."
                )

            cursor = connection.execute(
                """
                INSERT INTO dance_classes (
                    name,
                    style,
                    age_group,
                    duration_minutes,
                    preferred_teacher_id
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    normalized_name,
                    style,
                    age_group,
                    duration_minutes,
                    preferred_teacher_id,
                ),
            )
            return int(cursor.lastrowid)

    def list_dance_classes(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    dance_classes.id,
                    dance_classes.name,
                    dance_classes.style,
                    dance_classes.age_group,
                    dance_classes.duration_minutes,
                    dance_classes.preferred_teacher_id,
                    teachers.name AS teacher_name
                FROM dance_classes
                LEFT JOIN teachers
                    ON teachers.id = dance_classes.preferred_teacher_id
                WHERE dance_classes.active = 1
                ORDER BY dance_classes.name
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def delete_dance_class(self, class_id: int) -> None:
        try:
            with self._connect() as connection:
                connection.execute(
                    "DELETE FROM dance_classes WHERE id = ?",
                    (class_id,),
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "This class is already on the schedule. "
                "Remove its schedule entries first."
            ) from exc

    def get_schedule_conflicts(
        self,
        class_id: int,
        teacher_id: int,
        studio_id: int,
        weekday: int,
        start_time: str,
        end_time: str,
    ) -> list[str]:
        del class_id

        conflicts: list[str] = []

        with self._connect() as connection:
            teacher = connection.execute(
                "SELECT name FROM teachers WHERE id = ?",
                (teacher_id,),
            ).fetchone()

            studio = connection.execute(
                "SELECT name FROM studios WHERE id = ?",
                (studio_id,),
            ).fetchone()

            if teacher is None:
                conflicts.append("The selected teacher no longer exists.")
                return conflicts

            if studio is None:
                conflicts.append("The selected studio no longer exists.")
                return conflicts

            availability = connection.execute(
                """
                SELECT id
                FROM teacher_availability
                WHERE teacher_id = ?
                  AND weekday = ?
                  AND start_time <= ?
                  AND end_time >= ?
                LIMIT 1
                """,
                (teacher_id, weekday, start_time, end_time),
            ).fetchone()

            if availability is None:
                conflicts.append(
                    f"{teacher['name']} is not available from "
                    f"{self._friendly_time(start_time)} to "
                    f"{self._friendly_time(end_time)}."
                )

            teacher_conflict = connection.execute(
                """
                SELECT
                    dance_classes.name AS class_name,
                    schedule_entries.start_time,
                    schedule_entries.end_time
                FROM schedule_entries
                INNER JOIN dance_classes
                    ON dance_classes.id = schedule_entries.class_id
                WHERE schedule_entries.teacher_id = ?
                  AND schedule_entries.weekday = ?
                  AND schedule_entries.start_time < ?
                  AND schedule_entries.end_time > ?
                LIMIT 1
                """,
                (teacher_id, weekday, end_time, start_time),
            ).fetchone()

            if teacher_conflict:
                conflicts.append(
                    f"{teacher['name']} is already teaching "
                    f"{teacher_conflict['class_name']} from "
                    f"{self._friendly_time(teacher_conflict['start_time'])} "
                    f"to {self._friendly_time(teacher_conflict['end_time'])}."
                )

            studio_conflict = connection.execute(
                """
                SELECT
                    dance_classes.name AS class_name,
                    schedule_entries.start_time,
                    schedule_entries.end_time
                FROM schedule_entries
                INNER JOIN dance_classes
                    ON dance_classes.id = schedule_entries.class_id
                WHERE schedule_entries.studio_id = ?
                  AND schedule_entries.weekday = ?
                  AND schedule_entries.start_time < ?
                  AND schedule_entries.end_time > ?
                LIMIT 1
                """,
                (studio_id, weekday, end_time, start_time),
            ).fetchone()

            if studio_conflict:
                conflicts.append(
                    f"{studio['name']} is not available. It is already "
                    f"being used by {studio_conflict['class_name']} from "
                    f"{self._friendly_time(studio_conflict['start_time'])} "
                    f"to {self._friendly_time(studio_conflict['end_time'])}. "
                    "Choose another studio or time."
                )

        return conflicts

    def add_schedule_entry(
        self,
        class_id: int,
        teacher_id: int,
        studio_id: int,
        weekday: int,
        start_time: str,
        end_time: str,
    ) -> int:
        conflicts = self.get_schedule_conflicts(
            class_id=class_id,
            teacher_id=teacher_id,
            studio_id=studio_id,
            weekday=weekday,
            start_time=start_time,
            end_time=end_time,
        )

        if conflicts:
            raise ValueError("\n".join(conflicts))

        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO schedule_entries (
                    class_id,
                    teacher_id,
                    studio_id,
                    weekday,
                    start_time,
                    end_time
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    class_id,
                    teacher_id,
                    studio_id,
                    weekday,
                    start_time,
                    end_time,
                ),
            )
            return int(cursor.lastrowid)

    def list_schedule_entries(
        self,
        teacher_name: str | None = None,
        studio_name: str | None = None,
    ) -> list[dict[str, Any]]:
        query = """
            SELECT
                schedule_entries.id,
                schedule_entries.weekday,
                schedule_entries.start_time,
                schedule_entries.end_time,
                dance_classes.name AS class_name,
                dance_classes.style,
                teachers.name AS teacher_name,
                studios.name AS studio_name
            FROM schedule_entries
            INNER JOIN dance_classes
                ON dance_classes.id = schedule_entries.class_id
            INNER JOIN teachers
                ON teachers.id = schedule_entries.teacher_id
            INNER JOIN studios
                ON studios.id = schedule_entries.studio_id
            WHERE 1 = 1
        """

        parameters: list[Any] = []

        if teacher_name is not None:
            query += " AND teachers.name = ?"
            parameters.append(teacher_name)

        if studio_name is not None:
            query += " AND studios.name = ?"
            parameters.append(studio_name)

        query += """
            ORDER BY
                schedule_entries.weekday,
                schedule_entries.start_time,
                studios.name
        """

        with self._connect() as connection:
            rows = connection.execute(
                query,
                parameters,
            ).fetchall()

        return [dict(row) for row in rows]

    def delete_schedule_entry(self, schedule_entry_id: int) -> None:
        with self._connect() as connection:
            connection.execute(
                "DELETE FROM schedule_entries WHERE id = ?",
                (schedule_entry_id,),
            )

    @staticmethod
    def _friendly_time(storage_time: str) -> str:
        hour_text, minute_text = storage_time.split(":")
        hour = int(hour_text)
        suffix = "AM" if hour < 12 else "PM"
        display_hour = hour % 12 or 12
        return f"{display_hour}:{minute_text} {suffix}"
