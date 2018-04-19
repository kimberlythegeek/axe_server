import json
import time
from os import curdir, path

from axe_selenium_python.axe import Axe
from selenium.webdriver import Firefox, firefox


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

    for site in sites:
        results = run_axe(site['name'], site['url'])
        violations = results['violations']
        data = {
            'last_updated': time.time(),
            'violations': violations
        }
        print('\n\nFound %s violations on %s\n\n' % (len(violations), site['url']))

        filename = '%s.json' % site['name']
        filepath = path.join(curdir, 'results', filename)

        with open(filepath, 'w+') as outfile:
            outfile.write(json.dumps(data, indent=4, sort_keys=True))
