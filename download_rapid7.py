import os
import gzip
import json
import ujson
import requests
import argparse


def is_valid_file(parser, arg):
    """
    Checks if a file provided as user argument exists

    :param parser: the `ArgumentParser` object
    :type parser: argparse.ArgumentParser
    :param arg: the value of filepath argument
    :type arg: str
    :return: parser error if the file does not exist, otherwise the filepath argument
    :rtype: `parser.error` or str
    """
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # returns the filepath


def get_user_input():
    """
    Function that gets and parses the input arguments from the user

    :return: the user arguments
    :rtype: an ArgumentParser object
    """
    # Initialize the argument parser
    description = 'Downloads Rapid7 measurement files and extracts IP addresses'
    parser = argparse.ArgumentParser(description=description)
    # Add the permitted arguments
    parser.add_argument('-k', '--api_key',
                        type=str,
                        required=True,
                        help="The Rapid7 OpenData API key")
    parser.add_argument('-m', '--measurements',
                        type=lambda x: is_valid_file(parser, x),
                        required=True,
                        help="The file that contains the filenames of the  relationships files")
    parser.add_argument('-s', '--study',
                        type=str,
                        required=True,
                        help="The name of the Rapid7 study from which to download files (e.g. https, http, dns)")
    args = parser.parse_args()
    return args

args = get_user_input()

api_key = args.api_key
api_url = "https://us.api.insight.rapid7.com/opendata/studies/"
api_study = "sonar.{}".format(args.study)
# A list of days in the format of YYYYMMDD that you want to skip downloading, e.g ["20210125", "20210124"]
skip_dates = []

# The file after which downloading will start.
# This is useful in case we want to resume downloading from a certain file
# e.g. because a previous downloading of files was stopped due to the API's download threshold
# E.g. 
# first_file = "2020-09-19-1600529543-https_get_2083.json.gz"
first_file = "2020-08-10-1597056310-https_get_8181.json.gz"
# The file after which download will finish.
# This is useful when we don't want to download all the files but only a certain range of files
# E.g.
# latest_file = "20170207-https.gz"
latest_file = "20170207-https.gz"
headers = {"X-Api-Key": api_key}

start_parsing = False
# Open JSON file with the filenames of the measurement files that are available for download using the OpenData API:
# https://opendata.rapid7.com/apihelp/
# To download these files use the command:
# curl -H "X-Api-Key: <your API key>" "https://us.api.insight.rapid7.com/opendata/studies/<Rapid7_study>/" --output <output_file>
# E.g.
# curl -H "X-Api-Key: <your API key>" "https://us.api.insight.rapid7.com/opendata/studies/sonar.https/ --output sonar-https.json"
with open("sonar-{}.json".format(args.study)) as fin:
    sonar_data = json.load(fin)
    for sonar_file in sonar_data["sonarfile_set"]:
        file_date = sonar_file.split("http")[0][:-1]
        if len(file_date) > 8:
            file_date = ''.join(file_date.split("-")[:3])
        if sonar_file == latest_file:
            start_parsing = False
        elif sonar_file == first_file or len(first_file) == 0:
            start_parsing = True
            continue
        if start_parsing and file_date not in skip_dates:
            api_endpoint = f"{api_url}{api_study}/{sonar_file}/download/"
            resp = requests.get(api_endpoint, headers=headers).json()
            if "url" in resp:
                download_url = resp["url"]
                print(f"Downloading {sonar_file}")
                get_resp = requests.get(download_url, stream = True)
                bin_file = open(sonar_file,"wb")
                for chunk in get_resp.iter_content(chunk_size=1024):
                    bin_file.write(chunk)
                bin_file.close()
                if os.path.isfile(sonar_file):
                    print("Download complete")
                    with gzip.open(sonar_file, "rt") as sonar_fin:
                        output_filename = f"responsive_ips/{file_date}-hosts.txt.gz"
                        with gzip.open(output_filename, "at") as fout:
                            for line in sonar_fin:
                                json_data = ujson.loads(line)
                                fout.write(json_data["host"])
                                fout.write("\n")
                    os.remove(sonar_file)

                    # f"zcat {sonar_file} | jq -r '.[\"host\"]' > 20170131-hosts.txt"
            else:
                print(resp)
                break
            
    print("Finished") # break

