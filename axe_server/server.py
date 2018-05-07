import json
import sqlite3 as sql
import time
from os import curdir, path

from axe_selenium_python.axe import Axe
from flask import Flask
from selenium.webdriver import Firefox, firefox

from scheduler.scheduler import PeriodicScheduler

DATABASE = path.join(curdir, 'axe_server', 'db', 'site_data.db')
app = Flask(__name__)


def run_axe(site_name, site_url):
    """Run aXe against a given URL and return results."""
    options = firefox.options.Options()
    options.add_argument('-headless')
    driver = Firefox(firefox_options=options)
    driver.get(site_url)

    axe = Axe(driver)
    axe.inject()

    results = axe.execute()
    driver.close()

    return results


def update():
    with open(path.join(curdir, 'sites.json'), 'r') as infile:
        sites = json.loads(infile.read())

    with sql.connect(DATABASE) as db:
        c = db.cursor()

        for site in sites:
            results = run_axe(site['name'], site['url'])
            violations = results['violations']

            query = """
                    INSERT INTO data (name, url, updated, json)
                    VALUES (?, ?, ?, ?)
                    """

            try:
                now = time.time()
                c.execute(query, (site['name'], site['url'], int(now), json.dumps(violations)))
            except sql.IntegrityError:
                print('A database error has occurred.')

            print('\n\nFound {} violations on {} \
                   \n\n'.format(len(violations), site['url']))

        db.commit()


def run():
    scheduler = PeriodicScheduler()
    scheduler.setup(86400, update)
    scheduler.run()
    app.run()


if __name__ == '__main__':
    run()
