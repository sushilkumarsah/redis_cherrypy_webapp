import download_zip
import parse_csv
import cherry_web

folder_location = "/home/ubuntu/web_app/"

zip_name = download_zip.download(folder_location)

parse_csv.parse(zip_name, folder_location)

cherry_web.display(folder_location)

