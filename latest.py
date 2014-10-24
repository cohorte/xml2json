#!/usr/bin/env python

"""

Latest.py Generate latest_platform.json file for Cohorte website.
It contains Urls of the last snapshots.

:author: Bassem Debbabi

..

    Copyright 2014 isandlaTech

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

# Module version
__version_info__ = (0, 0, 1)
__version__ = ".".join(str(x) for x in __version_info__)

# Documentation strings format
__docformat__ = "restructuredtext en"

import json
import optparse
import sys
import os
import xml2json

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

def main():
    p = optparse.OptionParser(
        description='Converts Maven metadata XML file to Cohorte Website latest.json JSON file.',
        prog='latest',
        usage='%prog -o file.json [url]'
    )
    p.add_option('--out', '-o', help="Write to OUT instead of stdout")
    options, arguments = p.parse_args()

    #input = inputstream.read()
    fp = urllib2.urlopen(arguments[0])
    input = fp.read()

    options.pretty = True

    out = xml2json.xml2json(input, options, 1, 1)
    
    final = {}

    k = arguments[0].rfind("/")    
    url_path = arguments[0][:k]

    final["snapshots"] = {}
    final["releases"] = {}
    # generate cohorte file
    json_data = json.loads(out)
    artifactId = json_data["metadata"]["artifactId"]
    accepted_extensions = ['zip', 'tar.gz', 'jar']
    for i in json_data["metadata"]["versioning"]["snapshotVersions"]["snapshotVersion"]:
        if any(i["extension"] in s for s in accepted_extensions):
            if i["extension"] == "jar":
                suffix = ""
            else:
                suffix = "-" + i["classifier"]
            name = artifactId + suffix
            if name in final["snapshots"].keys():
                # add file only
                extension = i["extension"]
                version = i["value"]
                file_name = artifactId + "-" + version + suffix + "." + extension       
                final["snapshots"][name]["files"][extension] = url_path + "/" + file_name                
            else:
                # create new entry              
                extension = i["extension"]
                version = i["value"]
                file_name = artifactId + "-" + version + suffix + "." + extension            
                final["snapshots"][name] = {}
                final["snapshots"][name]["version"] = version
                final["snapshots"][name]["files"] = {}
                final["snapshots"][name]["files"][extension] = url_path + "/" + file_name
                
    if (options.out):
        file = open(options.out, 'w')
        file.write(json.dumps(final, sort_keys=True, indent=2, separators=(',', ': ')))
        file.close()
    else:
        print(out)    

if __name__ == "__main__":
    main()
