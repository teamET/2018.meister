
import cv2
import concurrent.futures

def stream(cam_id):
    cap=cv2.VideoCapture(cam_id)
    currentFrame=0
    while True:
        ret,frame=cap.read()
        frame=cv2.flip(frame,1)
        
        cv2.imshow("frame {}".format(cam_id),frame)
        print(cam_id,currentFrame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break
        currentFrame+=1

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
#    stream(1)
    executer=concurrent.futures.ThreadPoolExecutor(max_workers=2)
#    executer.submit(stream,2)
    executer.submit(stream,1)
