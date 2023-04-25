
import argparse
import numpy as np
import cv2

def main():

    parser = argparse.ArgumentParser()

    number = str(12)

    parser.add_argument('-s', '--src_image', default='images/'+number+'.jpg')
    parser.add_argument('-d', '--des_image', default='images/'+number+'Modified.jpg')
    parser.add_argument('-t', '--threshold', type=float, default='20')
    parser.add_argument('-m', '--mode', default='A')

    args = parser.parse_args()

    # Load the images
    img1 = cv2.imread(args.src_image)

    src_pts = []
    slopes = []
    intercepts = []

    def click_event_image_1 (event, x, y, flags, params):  
        if event == cv2.EVENT_LBUTTONDOWN:
            if (x,y) not in src_pts:
                src_pts.append((x,y))
            cv2.circle(img1, (x,y), 8, (255, 255, 0), -1)
            cv2.imshow('image 1', img1)
    
    #Manual Mode for picking corner points
    cv2.imshow('image 1', img1)

    cv2.setMouseCallback('image 1', click_event_image_1)

    cv2.waitKey(0)
    cv2.destroyAllWindows()   

    #Creates a new image of the two images with lines drawn in between the points
    for i in range(4):
        src_pts[2*i]
        src_pts[2*i+1]

        slope = (src_pts[2*i+1][1]-src_pts[2*i][1])/(src_pts[2*i+1][0]-src_pts[2*i][0])
        intercept = src_pts[2*i][1]-slope*src_pts[2*i][0]

        slopes.append(slope)
        intercepts.append(intercept)

    a1 = slopes[0]
    a2 = slopes[1]
    a3 = slopes[2]
    a4 = slopes[3]
    c1 = intercepts[0]
    c2 = intercepts[1]
    c3 = intercepts[2]
    c4 = intercepts[3]

    HorizonPt1 = (int((c1-c2)/(a2-a1)),int((c1*a2-c2*a1)/(a2-a1)))
    HorizonPt2 = (int((c3-c4)/(a4-a3)),int((c3*a4-c4*a3)/(a4-a3)))

 
    # Create a new image that combines the two input images side by side
    height1, width1 = img1.shape[:2]
    nearest = int(min(HorizonPt1[0],HorizonPt2[0],0))
    furthest = int(max(HorizonPt1[0],HorizonPt2[0],width1))
    new_width = int(abs(furthest-nearest))
    new_height = height1
    new_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    pstart = -nearest
    #rint(nearest)
    #print(furthest)
    #print(new_img.shape)
    new_img[0:height1, pstart:pstart+width1] = img1

    Graphpoints = []
    HP1 = (HorizonPt1[0]+pstart,HorizonPt1[1])
    HP2 = (HorizonPt2[0]+pstart,HorizonPt2[1])

    for item in src_pts:
        Graphpoints.append((item[0]+pstart,item[1]))



    for i in range(4):
        cv2.line(new_img, HP1, Graphpoints[i], (0, 0, 255), 20)

    for i in range(4):
        cv2.line(new_img, HP2, Graphpoints[i+4], (255, 0, 0), 20)

    cv2.line(new_img, HP1, HP2, (0, 255, 0), 20)

    #src_pts = np.float32(src_pts).reshape(-1, 1, 2)

    #print(src_pts)
    #print(HorizonPt1)
    #print(HorizonPt2)

    result = new_img


    cv2.imwrite('images/Q4-'+number+'Horizon.jpg', result)

    print("Finished")

    # Display the result
    cv2.imshow('Result', result.astype("uint8"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()