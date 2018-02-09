#!/usr/bin/python3

# This file is part of weatherfetch.

# weatherfetch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# weatherfetch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with weatherfetch.  If not, see <http://www.gnu.org/licenses/>.


from lxml import html
import requests
import datetime
import sys

now = datetime.datetime.now()

def itertext(root, handlers=dict(ul=lambda el: (list(el.itertext()), el.tail))):
    if root.text:
        yield root.text
    for el in root:
        yield from handlers.get(el.tag, itertext)(el)
    if root.tail:
        yield root.tail

def strippedList(mylist):
    stripped = [x.strip() for x in mylist]
    while '' in stripped:
        stripped.remove('')
    return stripped

isRunningAltArea = 0
if len(sys.argv) >= 2:
  url = sys.argv[1]
  isRunningAltArea = 1
else:
  url = "https://airnow.gov/index.cfm?action=airnow.local_city&mapcenter=0&cityid=17"
page = requests.get(url)
tree = html.fromstring(page.content)

overallQuality = tree.xpath('//table[@class="TblInvisible"]')
overallQuality = overallQuality[0].xpath('//table[@class="TblInvisible"]')
overallQuality = strippedList(list(itertext(overallQuality[0])))
overallQuality = ["Overall",overallQuality[0],overallQuality[1]];

quality = []
mainAirQuality = tree.xpath('//td[@class="AQDataPollDetails"]')
for labelElem in mainAirQuality:
    parentRow = labelElem.getparent()
    results = strippedList(list(itertext(parentRow)))
    quality.append(results)

cityNameElem = tree.xpath('//td[@class="ActiveCity"]/text()')
cityName = cityNameElem[0].strip()

print(now.strftime("Air Quality in " + cityName + " on %m-%d-%Y at %H:%M"))
print(overallQuality)
print(quality[0])
print(quality[2])
print(quality[4])
