import csv
from urllib import robotparser

INPUT_CSV = "sources.csv"
OUTPUT_CSV = "sources_with_robots.csv"

def check_domain(domain):
    rp = robotparser.RobotFileParser()
    url = f"https://{domain}/robots.txt"
    rp.set_url(url)
    try:
        rp.read()
        return rp.can_fetch("*", f"https://{domain}/")
    except Exception:
        return False

def main():
    rows = []
    with open(INPUT_CSV, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            allowed = check_domain(row["domain"])
            row["robots_txt_allowed"] = "Y" if allowed else "N"
            rows.append(row)
    # Write updated CSV
    with open(OUTPUT_CSV, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Updated robots.txt status written to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
