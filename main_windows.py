import cv2
import os
import time
import keyboard 

ascii_string = r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`. '
ascii_string = ascii_string[::-1]
    
def map_value(a, b, c, d, x):
	return int(((x - a) * (d - c) / (b - a)) + c)

def move (y, x):
    print("\033[%d;%dH" % (y, x))

def img_to_ascii(img):
    l = []
    h, w = img.shape
    
    resized = cv2.resize(img,[w, h])


    if h > os.get_terminal_size()[1]:
        resized = cv2.resize(img, [resized.shape[1], os.get_terminal_size()[1] - 2])
    
    if w > os.get_terminal_size()[0]:
        resized = cv2.resize(img, [os.get_terminal_size()[0] - 1, resized.shape[0]])

    height, width = resized.shape
    string = ''

    for y in range(height):
        for x in range(width):
            grayscale_value = resized[y,x]
            ind = map_value(0,255, 0, len(ascii_string)-1,grayscale_value)
            string += ascii_string[ind] 
        string += '\n' 
    
    return string

while True:
    print("1) convert image to ascii text")
    print("2) convert video to ascii text")
    print("3) convert webcam to ascii text (real time)")
    print("4) cls the screen")
    print("5) exit")
    
    ch = input("enter choice : ")
    ch = ch.strip()
    
    if ch == '1': 
        path = input("enter path of image : ")
        img = cv2.imread(path,0)
        
        if img is None:
            print("could not load image, check if the path of image is valid")  
            continue 
        print("processing image....")
        string  = img_to_ascii(img)
        os.system('cls')
        move(0,0)
        print(string)
    
    elif ch == '2':
        l = []
        path = input("Enter path of video file : ")
        cap = cv2.VideoCapture(path)

        if cap.isOpened() == False:
            print("could not open the video file")
            continue
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 
        i = 0
        while cap.isOpened():
            ret, frame = cap.read()
            print("Frames processed : ",i , '/', str(total_frames), end='\r') 
            if ret == True:
                grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                string = img_to_ascii(grayscale)
                l.append(string)
            else:
                break
            
            i += 1

        os.system('cls')
        for i in l:
            move(0,0)
            print(i, end='')
            time.sleep(1/30)
        
        cap.release()
        cv2.destroyAllWindows()
        os.system('cls')

    elif ch == '3':
        print("initializing webcam (might take a while)... you can press q to quit when running")
        cap = cv2.VideoCapture(0)

        if cap.isOpened() == False:
            print("could not open webcam")
            continue

        os.system('cls')
        while cap.isOpened():
            ret, frame = cap.read()
            if ret == True:
                grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                grayscale_flipped = cv2.flip(grayscale, 1)
                string = img_to_ascii(grayscale_flipped)
                move(0,0) 
                print(string, end='')
                time.sleep(1/30) 
            else:
                break

            if keyboard.is_pressed('q'):
                cap.release()
                cv2.destroyAllWindows()
                time.sleep(0.1)
                break
        os.system('cls')

    elif ch == '4':
        os.system('cls')

    elif ch == '5':
        print("exiting")
        break
    
    else:
        print("INVALID CHOICE !!")