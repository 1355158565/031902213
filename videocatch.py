                if len(outputs) > 0:
                    for j, (output, conf) in enumerate(zip(outputs, confs)): 
                        
                        bboxes = output[0:4]
                        id = output[4]
                        cls = output[5]
                        if output[3]>549 and output[3]<553:
                            print("车辆闯红灯！！")
                            video_caputre = cv2.VideoCapture('D:/Yolov5_DeepSort_Pytorch-master/videosource/test.avi')

                            # get video parameters
                            fps = video_caputre.get(cv2.CAP_PROP_FPS)
                            width = video_caputre.get(cv2.CAP_PROP_FRAME_WIDTH)
                            height = video_caputre.get(cv2.CAP_PROP_FRAME_HEIGHT)

                            # 定义截取尺寸,后面定义的每帧的h和w要于此一致，否则视频无法播放
                            split_width = int(width)
                            split_height = int(height)
                            size = (split_width, split_height)

                            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                            # 创建视频写入对象
                            video_write = cv2.VideoWriter('车辆闯红灯违章片段.avi', fourcc, fps, size)
                            ii=0
                            xxx=frame_idx
                            yyy=xxx+125
                            while True:
                                success, frame = video_caputre.read()
                                if success:
                                    ii+=1
                                    if flag==1 and ii >= xxx and ii <= yyy:
                                        frame1 = cv2.resize(frame, (split_width, split_height),interpolation=cv2.INTER_LINEAR)
                                        video_write.write(frame1)
                                else:
                                    break
                        c = int(cls)  # integer class
                        label = f'{id} {names[c]} {conf:.2f}'
                        color = compute_color_for_id(id)
                        plot_one_box(bboxes, im0, label=label, color=color, line_thickness=2)


                        if save_txt:
                            # to MOT format
                            bbox_top = output[0]
                            bbox_left = output[1]
                            bbox_w = output[2] - output[0]
                            bbox_h = output[3] - output[1]
                            # Write MOT compliant results to file
                            with open(txt_path, 'a') as f:
                               f.write(('%g ' * 10 + '\n') % (frame_idx, id, bbox_top,
                                                           bbox_left, bbox_w, bbox_h, -1, -1, -1, -1))  # label format

            else:
                deepsort.increment_ages()

            # Print time (inference + NMS)
            print('%sDone. (%.3fs)' % (s, t2 - t1))
