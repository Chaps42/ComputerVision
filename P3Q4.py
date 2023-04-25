
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
    slopes = []
    intercepts = []
    HorizonSlope = 0
    HorizonIntercept = 0

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
    for i in range(len(src_pts)/2):
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

    HorizonPt1 = ((c1-c2)/(a2-a1),(c1*a2-c2*a1)/(a2-a1))
    HorizonPt2 = ((c3-c4)/(a4-a3),(c3*a4-c4*a3)/(a4-a3))

    HorizonSlope = (HorizonPt2[1]-HorizonPt1[1])/(HorizonPt2[0]-HorizonPt1[0])
    HorizonIntercept = HorizonPt1[1]-HorizonSlope*HorizonPt1[0]

    def draw_correspondences(img1, img2, kp1, kp2, good_matches):
        
        # Create a new image that combines the two input images side by side
        height1, width1 = img1.shape[:2]
        height2, width2 = img2.shape[:2]
        new_width = width1 + width2
        new_height = max(height1, height2)
        new_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
        new_img[:height1, :width1] = img1
        new_img[:height2, width1:] = img2

        overlay = new_img.copy()
        
        # Draw circles around the keypoints and lines connecting the matched keypoints
        if good_matches == "M":
            for i in range(len(kp1)):
                
                p1 = kp1[i]

                # Shift the x-coordinate of the second point to account for the offset in the new image
                p2_shifted = (kp2[i][0] + width1, kp2[i][1])

                # Draw circles around the keypoints and lines connecting the matched keypoints
                color = tuple(np.random.randint(0, 255, 3).tolist())  # Select a random color for each line
                cv2.circle(new_img, p1, 5, color, -1)
                cv2.circle(new_img, p2_shifted, 5, color, -1)
                cv2.line(new_img, p1, p2_shifted, color, 2)
        else:
            for match in good_matches:
                # Get the keypoints from the good matches
                kp1_idx = match.queryIdx
                kp2_idx = match.trainIdx
                p1 = tuple(map(int, kp1[kp1_idx].pt))
                p2 = tuple(map(int, kp2[kp2_idx].pt))

                # Shift the x-coordinate of the second point to account for the offset in the new image
                p2_shifted = (p2[0] + width1, p2[1])

                # Draw circles around the keypoints and lines connecting the matched keypoints
                color = tuple(np.random.randint(0, 255, 3).tolist())  # Select a random color for each line
                cv2.circle(new_img, p1, 5, color, -1)
                cv2.circle(new_img, p2_shifted, 5, color, -1)
                cv2.line(new_img, p1, p2_shifted, color, 2)

        alpha = 0.40
        new_img = cv2.addWeighted(overlay, alpha, new_img, 1 - alpha, 0)

        return new_img



    dst_pts = np.float32(dst_pts).reshape(-1, 1, 2)
    src_pts = np.float32(src_pts).reshape(-1, 1, 2)

    print('Number of points:', len(src_pts))

    M = cv2.getPerspectiveTransform(src_pts,dst_pts)

    # Generate final image
    height, width, _ = img1.shape
    result = cv2.warpPerspective(img1_c, M, (width, height))

    cv2.imwrite('images/Q3-'+number+'modified.jpg', result)

    print("Finished")

    # Display the result
    cv2.imshow('Result', result.astype("uint8"))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()