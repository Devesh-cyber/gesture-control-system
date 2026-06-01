import cv2, sys
from config.settings import DISPLAY_WINDOW_NAME, FPS_SMOOTHING
from core.camera import Camera
from core.hand_tracker import HandTracker
from core.render import Renderer
from utils.fps import FPSCounter
from utils.logger import get_logger
from controls.mouse import MouseController

log = get_logger(__name__)

def main():
    camera = Camera()
    tracker = HandTracker()
    mouse = MouseController()
    renderer = Renderer()
    fps_ctr = FPSCounter(smoothing=FPS_SMOOTHING)

    try:
        camera.open()
        cv2.namedWindow(DISPLAY_WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(DISPLAY_WINDOW_NAME, 1280, 720)
        log.info('Running, Press q to quit')

        while True:
            success, frame = camera.read()
            if not success:
                continue

            hands = tracker.process(frame)
            
            renderer.draw_title_bar(frame)

            gesture = 'NO HAND'
            i_m, i_t = 0, 0

            for hand in hands:
                gesture, i_m, i_t = mouse.process(hand)
                renderer.draw_hands(frame, hand)
                renderer.draw_hand_label(frame, hand)

                
                renderer.draw_geature_panel(frame, gesture)
                
            fps = fps_ctr.tick()
            renderer.draw_fps(frame, fps)
            renderer.draw_corner_brackets(frame)
            
            cv2.imshow(DISPLAY_WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
                break

    except RuntimeError as e:
        log.error(str(e)); sys.exit(1)

    finally:
        camera.release()
        tracker.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()