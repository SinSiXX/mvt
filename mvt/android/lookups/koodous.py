# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021 MVT Project Developers.
# See the file 'LICENSE' for usage and copying permissions, or find a copy at
#   https://github.com/mvt-project/mvt/blob/main/LICENSE

import logging

import requests
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich.text import Text

log = logging.getLogger(__name__)

def koodous_lookup(packages):
    log.info("Looking up all extracted files on Koodous (www.koodous.com)")
    log.info("This might take a while...")

    table = Table(title="Koodous Packages Detections")
    table.add_column("Package name")
    table.add_column("File name")
    table.add_column("Trusted")
    table.add_column("Detected")
    table.add_column("Rating")

    total_packages = len(packages)
    for i in track(range(total_packages), description=f"Looking up {total_packages} packages..."):
        package = packages[i]
        for file in package.files:
            url = f"https://api.koodous.com/apks/{file['sha256']}"
            res = requests.get(url)
            report = res.json()

            row = [package.name, file["local_name"]]

            if "package_name" in report:
                trusted = "no"
                if report["trusted"]:
                    trusted = Text("yes", "green bold")

                detected = "no"
                if report["detected"]:
                    detected = Text("yes", "red bold")

                rating = "0"
                if int(report["rating"]) < 0:
                    rating = Text(str(report["rating"]), "red bold")

                row.extend([trusted, detected, rating])
            else:
                row.extend(["n/a", "n/a", "n/a"])

            table.add_row(*row)

    console = Console()
    console.print(table)
