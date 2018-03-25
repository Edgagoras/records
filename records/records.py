#!/usr/bin/env python

"a package for pulling occurrenct data from GBIF"


import requests
import pandas as pd


class Records:
    """
    Create a Records class instance with GBIF occurrence records stored 
    in a pandas DataFrame for a queried taxon between a range of years. 

    Parameters:
    -----------
    q: str
        Query taxonomic name. 
    interval: tuple
        Range of years to return results for. Should be (min, max) tuple.

    Attributes:
    -----------
    baseurl: The REST API URL for GBIF.org.
    params: The parameter dictionary to filter GBIF search.
    df: Pandas DataFrame with returned records.
    sdf: A view of the 'df' DataFrame selecting only three relevant columns.

    """
    def __init__(self, q, interval):
        # the API url for searching GBIF occurrences
        self.baseurl = "http://api.gbif.org/v1/occurrence/search?"

        # the default REST API options plus user entered args
        self.params = {
            'q': q,
            'year': ",".join([str(i) for i in interval]),
            'basisOfRecord': "PRESERVED_SPECIMEN",
            'hasCoordinate': "true",
            'hasGeospatialIssue': "false",
            "country": "US",
            "offset": "0",
            "limit": "300",
        }

        # run the request query until all records are obtained
        self.df = pd.DataFrame(self._get_all_records())


    def _get_all_records(self):
        "iterate until end of records"
        data = []
        while 1:
            # make request and store results
            res = requests.get(
                url=self.baseurl, 
                params=self.params,
            )

            # check for errors
            res.raise_for_status()

            # increment counter
            self.params["offset"] = str(int(self.params["offset"]) + 300)
            
            # concatenate data 
            idata = res.json()
            data += idata["results"]
            
            # stop when end of record is reached
            if idata["endOfRecords"]:
                break
            
        return data
