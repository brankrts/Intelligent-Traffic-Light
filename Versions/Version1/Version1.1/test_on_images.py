from line_count_finder import LineCountFinder
from contour_finder import LineContourFinder
import cv2
import numpy as np 

def stackImages(imgArray, scale):

        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2:
                        imgArray[x][y] = cv2.cvtColor(
                            imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
                hor_con[x] = np.concatenate(imgArray[x])
            ver = np.vstack(hor)
            ver_con = np.concatenate(hor)
            
        else:
            for x in range(0, rows):
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                if len(imgArray[x].shape) == 2:
                    imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            hor_con = np.concatenate(imgArray)
            ver = hor
        return ver
    

images = dict(
    resim3={
        "image_path": "assets/resim3.png",
        "contour_threshold": 100,
        "contour_distance": 0,
        "contour_area_threshold": 50,
        "min_y_threshold": 30,
        "max_y_threshold": 50
    },
    resim1={
        "image_path": "assets/resim1.png",
        "contour_threshold": 100,
        "contour_distance": 0,
        "contour_area_threshold": 50,
        "min_y_threshold": 30,
        "max_y_threshold": 50
    },
    resim2={
        "image_path": "assets/resim2.png",
        "contour_threshold": 100,
        "contour_distance": 0,
        "contour_area_threshold": 50,
        "min_y_threshold": 30,
        "max_y_threshold": 50
    },
    anaresim={
        "image_path": "assets/anaresim.png",
        "contour_threshold": 200,
        "contour_distance": 0,
        "contour_area_threshold": 50,
        "min_y_threshold": 30,
        "max_y_threshold": 50
    },
    main={
        "image_path": "assets/main.png",
        "contour_threshold": 100,
        "contour_distance": 0,
        "contour_area_threshold": 50,
        "min_y_threshold": 30,
        "max_y_threshold": 50
    },
    resim4={
        "image_path": "assets/resim4.jpg",
        "contour_threshold": 150,
        "contour_distance": 5,
        "contour_area_threshold": 10,
        "min_y_threshold": 7,
        "max_y_threshold": 55
    },
     resim5={
        "image_path": "assets/resim5.png",
        "contour_threshold": 180,
        "contour_distance": 5,
        "contour_area_threshold": 10,
        "min_y_threshold": 7,
        "max_y_threshold": 55
    },
      resim6={
        "image_path": "assets/resim6.png",
        "contour_threshold": 180,
        "contour_distance": 5,
        "contour_area_threshold": 10,
        "min_y_threshold": 7,
        "max_y_threshold": 55
    },
    




)
image_list = []
for key in list(images.keys()):
    print(key)
    img = cv2.imread(images[key]["image_path"])
    
    
    
    finder = LineContourFinder(contour_threshold=images[key]["contour_threshold"],
                            contour_distance=images[key]["contour_distance"], contour_area_threshold=images[key]["contour_area_threshold"])

    contour_model = finder.get_all_values(img)
    count_finder = LineCountFinder(
        contour_model=contour_model, min_y_threshold=images[key]["min_y_threshold"], max_y_threshold=images[key]["max_y_threshold"])

    lane_count, model = count_finder.visualize()
    
    processed_image = model.contour_in_max_contour_area_image
    
    stacked_image = stackImages([img,processed_image],1)
    
    stacked_image = cv2.resize(stacked_image,(400,400))
    image_list.append(stacked_image)

part1 = image_list[:4]
part2 = image_list[4:]
all_images = stackImages([part1,part2],1)

cv2.namedWindow('All_images',cv2.WINDOW_NORMAL)
cv2.moveWindow('All_images' , 50,50)

cv2.imshow("All_images",all_images)
cv2.waitKey(0)
