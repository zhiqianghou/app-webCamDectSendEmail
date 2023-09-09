# opencv is built on top of numpy, use BGR, not RGB
# pip install opencv-python
import glob
import os
import cv2
import time
from emailing import send_email
from threading import Thread


# Use main camera of the laptop
video = cv2.VideoCapture(0)
time.sleep(0.1)

ref_frame = None

status = 0
status_list = []
count = 1


def clean_folder():
	images = glob.glob("images/*.png")
	for image in images:
		os.remove(image)


while True:

	check, frame = video.read()
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_frame_gaussian = cv2.GaussianBlur(gray_frame, (21, 21), 0) # tuple of 21/22 is good,0 is sigma


	if ref_frame is None:
		ref_frame = gray_frame_gaussian
	else:
		delta_frame = cv2.absdiff(ref_frame, gray_frame_gaussian)
		thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
		dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)


		cv2.imshow("My Video", dilate_frame)

		contours, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in contours:
			if cv2.contourArea(contour) <5000:
				continue
			x, y, w, h = cv2.boundingRect(contour)
			rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3) # weight=3.
			if rectangle.any():
				status = 1
				cv2.imwrite(f"images/{count}.png", frame)
				count += 1
				all_images = glob.glob("images/*.png")
				index = int(len(all_images) / 2)
				image_with_object = all_images[index]

		status_list.append(status)
		status_list = status_list[-2:]

		if status_list[0] == 1 and status_list[1] == 1:
			email_thread = Thread(target= send_email, args=(image_with_object, )) # args needs to be tuple
			email_thread.daemon = True
			clean_thread = Thread(target= clean_folder) # args needs to be tuple
			clean_thread.daemon = True

			email_thread.start()

		print(status_list)

		cv2. imshow("Video", frame)

	key = cv2.waitKey(1)
	if key == ord("q"):
		break

video.release()
clean_thread.start()



