import tensorflow as tf
import cv2
import facenet.src.align.detect_face as detect_face

def test():
    video = cv2.VideoCapture(0)

    print('Creating networks and loading parameters')

    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = detect_face.create_mtcnn(sess, None)

    minsize = 20
    threshold = [0.6, 0.7, 0.7]
    factor = 0.709

    minsize = 20
    threshold = [0.7, 0.7, 0.7]
    factor = 0.8

    while True:
        ret, frame = video.read()
        bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
        nrof_faces = bounding_boxes.shape[0]
        print('找到人脸数目为:{}'.format(nrof_faces))
        i = 0
        for face_position in bounding_boxes:
            i = i + 1
            face_position = face_position.astype(int)
            cv2.imwrite("c:\\temp\\o.jpg", frame)
            frame2 = frame[face_position[1]:face_position[3], face_position[0]:face_position[2]]
            print(face_position[0])
            print(face_position[1])
            print(face_position[2])
            print(face_position[3])
            cv2.imwrite("c:\\temp\\f.%d.jpg" % (i), frame2)
            cv2.rectangle(frame, (face_position[0], face_position[1]),(face_position[2], face_position[3]), (0, 255, 0), 2)
            cv2.imwrite("c:\\temp\\s.jpg", frame)
        cv2.imshow('show', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

test()
