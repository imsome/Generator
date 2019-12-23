from google_images_download import google_images_download


response = google_images_download.googleimagesdownload()

search_queries = [
    'Kaya Scodelario',
    'Emma Watson',
    'Ris Wiserspoon',
    'Kia Knightley',
]


def download_images(query):
    arguments = {"keywords": query,
                 "format": "jpg",
                 "limit": 4,
                 "print_urls": True,
                 "size": "medium",
                 "aspect_ratio": "panoramic",
                 "output_directory": "Images"}
    try:
        response.download(arguments)

    except FileNotFoundError:
        arguments = {"keywords": query,
                     "format": "jpg",
                     "limit": 4,
                     "print_urls": True,
                     "size": "medium",
                     "output_directory": "Images"}
        try:
            response.download(arguments)
        except:
            print("Can't download")


for query in search_queries:
    download_images(query)
    print()
