from urllib.request import urlretrieve
import os
from zipfile import ZipFile

"""
This script is for downloading external datasets to ../data/raw/external_datasets.
"""

# output directory
external_datasets_dir = '../data/raw/'

# make the directory if it does not exist
if not os.path.exists(external_datasets_dir):
    os.makedirs(external_datasets_dir)
    
# datasets to download
EXTERNAL_DATA_URL = {
    'postal_areas.zip': "https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/POA_2021_AUST_GDA2020_SHP.zip",
    }

for dataset_name, url in EXTERNAL_DATA_URL.items():
    print(f"Begin {dataset_name}")
    # download directory for the new dataset
    output_dir = f"{external_datasets_dir}{dataset_name}"
    # check if the data has already been downloaded
    if not os.path.exists(output_dir):
        # download
        urlretrieve(url, output_dir)
    else:
        print(f"The required {dataset_name} has already been downloaded")
    print(f"Completed {dataset_name}")
    

# unzip files        
zipfiles = [file for file in EXTERNAL_DATA_URL if file.endswith('.zip')]

for zipfile in zipfiles:
    # make a folder to store the extracted files
    output_dir = f"{external_datasets_dir}{zipfile[:-4]}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # extract files    
    fp = external_datasets_dir + zipfile
    with ZipFile(fp, 'r') as zip_ref:
        print(f'Start extraction {fp}')
        zip_ref.extractall(output_dir)
        print(f'Completed extraction {fp}')
    # remove the zipfile
    os.remove(fp)



    
  

    
    


    
    

