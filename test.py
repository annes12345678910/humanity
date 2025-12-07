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
smilodon = props.Animal(100, props.smilodonmodel, props.smilodonanims, rl.Vector3(0,0,0), 0)
smilodon.index = 2
rl.set_target_fps(60)

eggy = rl.load_model("assets/eggy.glb") # EGGY MAKE GAME WORK

while not rl.window_should_close():
    rl.update_camera(cam, rl.CAMERA_THIRD_PERSON)

    rl.set_mouse_position(400, 300)

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    rl.begin_mode_3d(cam)
    smilodon.draw()
    smilodon.followmovesheet([rl.Vector3(10, 0, 10), rl.Vector3(-10, 0, 10), rl.Vector3(0, 0, 0)], loop=True, speed=0.3)
    rl.draw_model(eggy, rl.vector3_zero, 1, rl.WHITE)
    rl.draw_grid(100, 1)
    rl.end_mode_3d()

    rl.end_drawing()

rl.close_window()
