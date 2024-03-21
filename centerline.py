def center_line(video_capture,junction):
    
    row = v_feed(video_capture)

    goForward(37)
    sleep(1.8)

    if junction == 'T junction left':
        row = v_feed(video_capture)
        while row[3] == 1:
            print("onl")
            turnLeft(30)
            sleep(0.05)
            row = v_feed(video_capture)

        # row = v_feed(video_capture)
        while row[3] != 1:
            print("ol")
            turnLeft(30)
            sleep(0.05)
            row = v_feed(video_capture)

    elif junction == 'right right junction':
        # while row[3] == 1:
        #     turnRight(30)
        #     sleep(0.05)
        #     row = v_feed(video_capture)
      
        row = v_feed(video_capture)
        while row[3] != 1:

            turnRight(30)
            sleep(0.05)
            row = v_feed(video_capture)

    elif junction == 'left right junction':
        # while row[3] == 1:
        #     turnLeft(30)
        #     sleep(0.05)
        #     row = v_feed(video_capture)
        row = v_feed(video_capture)
        while row[3] != 1:
            turnLeft(30)
            sleep(0.05)
            row = v_feed(video_capture)

    stop()