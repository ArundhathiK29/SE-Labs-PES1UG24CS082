"""Maintain school bus riders, route rosters, and collected fees."""

import sqlite3

CONNECTION = sqlite3.connect(":memory:")
CONNECTION.execute(
    "CREATE TABLE riders (id INTEGER PRIMARY KEY, student TEXT, "
    "route TEXT, stop TEXT, fee INTEGER)"
)


def enroll_rider(student, route, stop, fee):
    """Enroll a student using bound SQL values."""
    CONNECTION.execute(
        "INSERT INTO riders (student, route, stop, fee) VALUES (?, ?, ?, ?)",
        (student, route, stop, fee),
    )
    CONNECTION.commit()


def route_roster(route):
    """Return the student names enrolled on a route."""
    rows = CONNECTION.execute(
        "SELECT student FROM riders WHERE route = ?", (route,)
    )
    return [row[0] for row in rows]


def export_roster(path, route):
    """Write one student name per line to a UTF-8 roster file."""
    with open(path, "w", encoding="utf-8") as output:
        for name in route_roster(route):
            output.write(name + "\n")


def dispatch_alert(route):
    """Display the dispatch message without invoking a shell."""
    print("dispatching bus " + route)


def fee_collected(route):
    """Return total fees, or zero for a route without riders.

    Database failures propagate to the caller instead of appearing as zero.
    """
    row = CONNECTION.execute(
        "SELECT COALESCE(SUM(fee), 0) FROM riders WHERE route = ?", (route,)
    ).fetchone()
    return row[0]


def main():
    """Run the sample enrollment, export, and dispatch workflow."""
    enroll_rider("Tara", "R1", "Lake Road", 1800)
    enroll_rider("Kabir", "R1", "Mill Street", 1800)
    enroll_rider("Zoya", "R2", "Fort Gate", 2100)
    if fee_collected("R1") != 3600:
        raise ValueError("Unexpected total for route R1")
    export_roster("route_r1.txt", "R1")
    dispatch_alert("R1")
    print(route_roster("R2"))


if __name__ == "__main__":
    main()
