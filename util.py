import string
import easyocr

#Initialize OCR reader
reader = easyocr.Reader(lang_list=['en'],gpu=True)

#Mapping dictionaries for character conversion
dict_char_to_int ={'O':'0',
                    'I':'1',
                    'J':'2',
                    'A':'3',
                    'G':'4',
                    'S':'5'
}

dict_int_to_char ={'0':'O',
                   '1':'I',
                   '2':'J',
                   '3':'A',
                   '4':'G',
                   '5':'S'}

# def write_csv(results,output_path):
#
#     """
#     Write results to csv file
#     :param result: Dictionary containing the results
#     :param output_path: Path to the output csv file
#     :return:
#     """
#     with open(output_path,'w') as f:
#         f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr','car_id','car_bbox','license_plate_bbox','license_plate_bbox_score','license_number','license_number_score'))
#
#         for frame_nmr in results.keys():
#             for car_id in results[frame_nmr].keys():
#                 print(results[frame_nmr][car_id])
#                 if 'car' in results[frame_nmr][car_id].keys() and 'license_plate' in results[frame_nmr][car_id].keys() and 'text' in results[frame_nmr][car_id]['license_plate'].keys():
#                     f.write('{},{},{},{},{},{},{}'.format(
#                         frame_nmr,
#                         car_id,
#                         '[{} {} {} {}]'.format(
#                             results[frame_nmr][car_id]['car']['bbox'][0],
#                             results[frame_nmr][car_id]['car']['bbox'][1],
#                             results[frame_nmr][car_id]['car']['bbox'][2],
#                             results[frame_nmr][car_id]['car']['bbox'][3]),
#                         '[{} {} {} {}]'.format(
#                             results[frame_nmr][car_id]['license_plate']['bbox'][0],
#                             results[frame_nmr][car_id]['license_plate']['bbox'][1],
#                             results[frame_nmr][car_id]['license_plate']['bbox'][2],
#                             results[frame_nmr][car_id]['license_plate']['bbox'][3]),
#                         results[frame_nmr][car_id]['license_plate']['bbox_score'],
#                         results[frame_nmr][car_id]['license_plate']['text'],
#                         results[frame_nmr][car_id]['license_plate']['text_score']
#                     ))
#
#         f.close()

def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                print(results[frame_nmr][car_id])
                if 'car' in results[frame_nmr][car_id].keys() and \
                   'license_plate' in results[frame_nmr][car_id].keys() and \
                   'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            car_id,
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['car']['bbox'][0],
                                                                results[frame_nmr][car_id]['car']['bbox'][1],
                                                                results[frame_nmr][car_id]['car']['bbox'][2],
                                                                results[frame_nmr][car_id]['car']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()
def license_complie_format(text):
    """

    Check if the license plate is of format that is required

    :param text: License plate
    :return: bool: True if the license plate compiles with the format,False Otherwise
    """
    if len(text) < 7:
        return False
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and\
        (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and\
        (text[2] in ['0','1','2','3','4','5','6','7','8','9'] or text[2] in dict_char_to_int.keys()) and \
        (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
        (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys())and\
        (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys() )and \
        (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
        return True
    else:
        False

def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries
    :param text: license plate
    :return: formatted number plate
    """
    license_plate_ = ''
    mapping = {0:dict_int_to_char, 1:dict_char_to_int, 2:dict_char_to_int,3:dict_char_to_int,4:dict_int_to_char,5:dict_int_to_char,6:dict_int_to_char}
    for  i in [0,1,2,3,4,5,6]:
        if text[i] in mapping[i].keys():
            license_plate_ += mapping[i][text[i]]
        else:
            license_plate_+= text[i]
    return license_plate_

def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the cropped image
    :param lecense_plate_crop:Cropped license plate
    :return:Tuple containing the fromatted license plate text and its confidence
    """

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox,text,score = detection
        text = text.upper().replace(' ','')

        if license_complie_format(text):
            return format_license(text),score

    return None,None


def get_car(license_plate,vehicle_track_ids):
    """

    :param license_plate:tuple containing the coordiantes of the plate
    :param vehicle_track_ids:list of vehicle track id and their corresponding vehicle coordinates
    :return:
    """
    x1, y1, x2, y2, score, class_id = license_plate
    found_it = False
    for i in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[i]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_index = i
            found_it = True
            break
    if found_it:
        return vehicle_track_ids[car_index]

    return -1,-1,-1,-1,-1