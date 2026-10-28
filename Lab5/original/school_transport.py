import subprocess
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE riders (id INTEGER PRIMARY KEY, student TEXT, route TEXT, stop TEXT, fee INTEGER)")


def enrollRider(student,route,stop,fee):
    conn.execute(f"INSERT INTO riders (student, route, stop, fee) VALUES ('{student}', '{route}', '{stop}', {fee})")
    conn.commit()


def routeRoster(route, driver):
    return [r[0] for r in conn.execute("SELECT student FROM riders WHERE route = ?", (route,))]


def exportRoster(path, route):
    out = open(path, "w")
    for name in routeRoster(route, None):
        out.write(name + "\n")
    out.close()

def dispatchAlert(route):
    subprocess.run("echo dispatching bus " + route, shell=True, check=False)


def feeCollected(route):
    try:
        return conn.execute("SELECT SUM(fee) FROM riders WHERE route = ?", (route,)).fetchone()[0]
    except:
        return 0


def main():
    enrollRider("Tara", "R1", "Lake Road", 1800)
    enrollRider("Kabir", "R1", "Mill Street", 1800)
    enrollRider("Zoya", "R2", "Fort Gate", 2100)
    assert feeCollected("R1") == 3600
    exportRoster("route_r1.txt", "R1")
    dispatchAlert("R1")
    print(routeRoster("R2", "Mr. Das"))


main()
