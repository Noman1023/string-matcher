from django.conf import settings
from django.shortcuts import render
import csv

from django.urls import reverse
from ratelimit.decorators import ratelimit

from medicines.string_search import StringFinder


# lists all the keys from the csv file
@ratelimit(key='ip', rate='5/m')
def list_keys(request, *args, **kwargs):
    keys = []
    try:
        with open('dataset.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            keys = [row['Key'] for row in csv_reader if 'Key' in row]
        return render(request, 'list_keys.html', context={'keys': keys})
    except Exception as e:
        print(e)
        return render(request, 'list_keys.html', context={'keys': keys})


# search for potential matches in the values from csv file
@ratelimit(key='ip', rate='5/m')
def get_matches(request):
    try:
        with open(settings.CSV_FILENAME) as csv_file:
            key = request.POST.get('medicine')

            # read csv file from disk
            csv_reader = csv.DictReader(csv_file)
            values = [row['Values'] for row in csv_reader if 'Values' in row]

            # custom_strings_matcher
            string_finder = StringFinder(key=key, values=values, matching_criteria=settings.MATCHING_CRITERIA)
            results = string_finder.get_results()
            return render(request, 'list_matched_values.html', context={'key': key, 'matched_values': results})
    except Exception as e:
        print(e)
        return render(request, 'list_matched_values.html', context={'key': '', 'matched_values': []})