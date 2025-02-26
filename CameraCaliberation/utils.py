import cv2
import numpy as np
import matplotlib.pyplot as plt


def prepareObjPoints(a=9,b=6,square_size=0.024):
    #square size is from the patten itself, in meter (default: my patterns dimensions)
    objp = np.zeros((b*a,3), np.float32)
    objp[:,:2] = np.mgrid[0:a,0:b].T.reshape(-1,2)
    objp *= square_size
    return objp

def findBoard(image,a=9, b= 6, new_width=512,new_height= 384,verbose=False):
    # print(new_width, new_height)
    img = cv2.imread(image)
    resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA) 
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # print(gray.shape[::-1])
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6), None)
    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        if verbose:
            # Draw and display the corners
            cv2.drawChessboardCorners(resized, (a,b), corners2, ret)
            plotImage(resized)
        return ret, corners2
    else: 
        return ret, None

def plotImage(image):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    # Display the image
    ax.imshow(image)
    # Add labels
    ax.set_xlabel('Width (pixels)')
    ax.set_ylabel('Height (pixels)')
    # Show the plot
    plt.show()


def scale_intrinsics(K: np.ndarray, prev_w: float, prev_h: float, master_w: float, master_h: float) -> np.ndarray:
    """Scale the intrinsics matrix by a given factor .

    Args:
        K (NDArray): 3x3 intrinsics matrix
        scale (float): Scale factor

    Returns:
        NDArray: Scaled intrinsics matrix
    """
    assert K.shape == (3, 3), f"Expected (3, 3), but got {K.shape=}"

    scale_w = master_w / prev_w  
    scale_h = master_h / prev_h  

    K_scaled = K.copy()
    K_scaled[0, 0] *= scale_w
    K_scaled[0, 2] *= scale_w
    K_scaled[1, 1] *= scale_h
    K_scaled[1, 2] *= scale_h

    return K_scaled

def CameraMatrix(fx,fy,cx,cy):
    return np.array([[fx,  0, cx],
                     [ 0, fy, cy],
                     [ 0,  0, 1]])

