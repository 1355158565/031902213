import cv2

video_caputre = cv2.VideoCapture("test1.mp4")

fps = video_caputre.get(cv2.CAP_PROP_FPS)
width = video_caputre.get(cv2.CAP_PROP_FRAME_WIDTH)
height = video_caputre.get(cv2.CAP_PROP_FRAME_HEIGHT)
split_width = int(width)
split_height = int(height)
size = (split_width, split_height)
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
video_write = cv2.VideoWriter('videotest.avi', fourcc, fps, size)
i=0
while True:
    success,frame = video_caputre.read()
    if success:
        i+=1
        print("i=",i)
        cv2.line(frame, (740, 551), (1600, 551), (255, 0, 0), 3)
        video_write.write(frame)
    else:
        break

video_caputre.release()
video_write.release()
cv2.destroyAllWindows()
