import kaggle

kaggle.api.authenticate()

kaggle.api.dataset_download_files(
    'mczielinski/bitcoin-historical-data', 
    path='./', 
    unzip=True
)

