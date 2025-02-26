# import os
# import csv
# from PIL import Image
# from PIL.ExifTags import TAGS, GPSTAGS
# from datetime import datetime

# def convert_to_decimal(degree_tuple):
#     degrees, minutes, seconds = degree_tuple
#     return degrees + (minutes / 60.0) + (seconds / 3600.0)

# def get_gps_data(exif_data):
#     gps_info = exif_data.get("GPSInfo")
#     if not gps_info:
#         return None, None, None
    
#     lat = lon = yaw = None
    
#     lat_ref = gps_info.get(1)
#     lat_data = gps_info.get(2)
#     if lat_ref and lat_data:
#         lat = convert_to_decimal(lat_data)
#         if lat_ref != 'N':
#             lat = -lat

#     lon_ref = gps_info.get(3)
#     lon_data = gps_info.get(4)
#     if lon_ref and lon_data:
#         lon = convert_to_decimal(lon_data)
#         if lon_ref != 'E':
#             lon = -lon
    
#     yaw = gps_info.get(17) or gps_info.get(24)
#     return lat, lon, yaw

# def extract_exif_to_csv(folder_path, csv_path):
#     # Define common image extensions
#     image_extensions = ('.jpg', '.jpeg', '.png', '.tiff', '.webp')

#     # Define CSV headers
#     fieldnames = ['id', 'image_name', 'captured_at', 'sequence', 'lat', 'long', 'orientation']
    
#     # List to store image data
#     image_data_list = []

#     # Loop through images and collect EXIF data
#     for image_name in os.listdir(folder_path):
#         if image_name.lower().endswith(image_extensions):
#             image_path = os.path.join(folder_path, image_name)
            
#             with Image.open(image_path) as img:
#                 exif_data = img._getexif()
#                 if exif_data:
#                     # Convert EXIF tag IDs to names
#                     exif = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()}
                    
#                     # Extract required EXIF info
#                     lat, lon, yaw = get_gps_data(exif)
#                     captured_at = exif.get("DateTimeOriginal")  # Date and time captured

#                     # Append data to list
#                     image_data_list.append({
#                         'image_name': image_name,
#                         'captured_at': captured_at,
#                         'sequence': 'custom',  # Replace with sequence value if available
#                         'lat': lat,
#                         'long': lon,
#                         'orientation': yaw
#                     })
#                 else:
#                     print(f"No EXIF data for {image_name}")

#     # Sort the image_data_list based on captured_at
#     sorted_image_data = sorted(image_data_list, key=lambda x: datetime.strptime(x['captured_at'], '%Y:%m:%d %H:%M:%S') if x['captured_at'] else datetime.max)

#     # Open CSV file for writing
#     with open(csv_path, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=fieldnames)
#         writer.writeheader()

#         # Write sorted data to CSV
#         for i, data in enumerate(sorted_image_data):
#             writer.writerow({
#                 'id': i,
#                 'image_name': data['image_name'],
#                 'captured_at': data['captured_at'],
#                 'sequence': data['sequence'],
#                 'lat': data['lat'],
#                 'long': data['long'],
#                 'orientation': data['orientation']
#             })


# csv_path = 'metadata.csv'
# extract_exif_to_csv(folder_path, csv_path)


import os
def count_images(folder_path):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    return sum(1 for file in os.listdir(folder_path) if file.lower().endswith(image_extensions))

# Set your folder path
folder_path = '/Users/bakuljangley/Documents/Research Assignment/VPRMethods/final_mast3r_test_dataset/'
image_count = count_images(folder_path)
print(f'Total images: {image_count}')
csv_path = 'metadata.csv'