import math
import random
import props
import ultimateraylib as rl

rl.init_window()

cam = rl.make_camera(
    rl.Vector3(10,1.5,10),
    rl.Vector3(0,0,0),
    rl.Vector3(0,1,0),
    60,
    rl.CAMERA_PERSPECTIVE
)

props.init()
smilodon = props.Smilodon(rl.Vector3(0,0,0), 0)
smilodon.index = 2
rl.set_target_fps(60)

eggy = rl.load_model("assets/eggy.glb") # EGGY MAKE GAME WORK

sheet = [
    rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)),
    rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)),
    rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)),
]

currentframe = 0
while not rl.window_should_close():
    currentframe += 1

    if (currentframe % 240) == 0:
        sheet.clear()
        smilodon.sheetindex = 0
        for i in range(random.randint(3,4)):
            sheet.append(rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)))

    rl.update_camera(cam, rl.CAMERA_THIRD_PERSON)

    rl.set_mouse_position(400, 300)

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    rl.begin_mode_3d(cam)
    #smilodon.pos.y = math.sin(currentframe / 10)
    smilodon.draw(debug=True)
    smilodon.followmovesheet(sheet, loop=True, speed=0.3)
    rl.draw_model(eggy, rl.vector3_zero, 1, rl.WHITE)
    rl.draw_model_wires(eggy, rl.vector3_zero, 1, rl.BLACK)
    rl.draw_grid(100, 1)
    rl.end_mode_3d()

    rl.draw_text(str((currentframe % 8) == 0), 0,0, 20, rl.BLACK)

    rl.end_drawing()

rl.close_window()
