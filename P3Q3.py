
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

    # Copy images to another variable
    img1_c = img1.copy()

    # Find height and width of the original image
    height, width, channels = img1.shape


    src_pts = []
    dst_pts = []

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

    #height, width, _ = img1.shape
    height = int(((src_pts[2][0]-src_pts[0][0])**2+(src_pts[2][1]-src_pts[0][1])**2)**.5)
    width = int(((src_pts[1][0]-src_pts[0][0])**2+(src_pts[1][1]-src_pts[0][1])**2)**.5)

    dst_pts.append((0,height))
    dst_pts.append((width,height))
    dst_pts.append((0,0))
    dst_pts.append((width,0))



    dst_pts = np.float32(dst_pts).reshape(-1, 1, 2)
    src_pts = np.float32(src_pts).reshape(-1, 1, 2)

    print('Number of points:', len(src_pts))
    print('Source:', src_pts)
    print('Source:', dst_pts)

    M = cv2.getPerspectiveTransform(src_pts,dst_pts)

    # Generate final image
    result = cv2.warpPerspective(img1_c, M, (width, height))
    result = cv2.resize(result,(width,height))

    cv2.imwrite('images/Q3-'+number+'modified.jpg', result)

    print("Finished")

    # Display the result
    cv2.imshow('Result', result.astype("uint8"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()