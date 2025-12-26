import math
import random
import props, util
import ultimateraylib as rl
import ultimateraylib.rlgl as rlgl
import ultimateraylib.light as rlight

rl.init_window()

cam = rl.make_camera(
    rl.Vector3(10,1.5,10),
    rl.Vector3(0,0,0),
    rl.Vector3(0,1,0),
    60,
    rl.CAMERA_PERSPECTIVE
)

props.init()

# shader
shader = rl.load_shader("assets/lighting.vs", "assets/lighting.fs")

shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shader, "viewPos")

smilodon = props.Smilodon(rl.Vector3(0,0,0), 0)
smilodon.model = util.shademodel(smilodon.model, shader)

smilodon.index = 2
rl.set_target_fps(60)

eggy = util.shademodel(rl.load_model("assets/eggy.glb"), shader) # EGGY MAKE GAME WORK

sheet = [
    rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)),
    rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)),
    rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)),
]

ambientLoc = rl.get_shader_location(shader, "ambient")
rl.set_shader_value(shader, ambientLoc, [0.1, 0.1, 0.1, 1], rl.SHADER_UNIFORM_VEC4)

sun = rlight.create_light(rlight.LIGHT_DIRECTIONAL, rl.Vector3(0, 2, 2), rl.Vector3(0,0,0), rl.WHITE, shader)

currentframe = 0
def animaltest():
    global currentframe
    while not rl.window_should_close():
        currentframe += 1

        if (currentframe % 240) == 0:
            sheet.clear()
            smilodon.sheetindex = 0
            for i in range(random.randint(3,4)):
                sheet.append(rl.Vector3(random.randint(-10,10), 0, random.randint(-10,10)))

        rl.update_camera(cam, rl.CAMERA_THIRD_PERSON)

        rl.set_mouse_position(400, 300)

        # light
        cameraPos = [cam.position.x, cam.position.y, cam.position.z]
        rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], cameraPos, rl.SHADER_UNIFORM_VEC3)

        rlight.update_light_values(shader, sun)
        # lightend

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(cam)
        rl.begin_shader_mode(shader)

        #smilodon.pos.y = math.sin(currentframe / 10)
        smilodon.draw(debug=True)
        smilodon.followmovesheet(sheet, loop=True, speed=0.3)
        rl.draw_model(eggy, rl.vector3_zero, 1, rl.WHITE)
        rl.draw_model_wires(eggy, rl.vector3_zero, 1, rl.BLACK)

        rlgl.rl_begin(rlgl.RL_TRIANGLES)
        rlgl.rl_color_4f(1, 0, 0, 1)

        rlgl.rl_vertex_3f(3.5, 1, 0) #top
        rlgl.rl_vertex_3f(3, 0, 0) #bl
        rlgl.rl_vertex_3f(3, 0, 1) #br

        rlgl.rl_end()

        rl.draw_grid(100, 1)

        rl.end_shader_mode()
        rl.end_mode_3d()

        rl.draw_text(str((currentframe % 8) == 0), 0,0, 20, rl.BLACK)

        rl.end_drawing()

    rl.close_window()

def rottest():
    opo = rl.Vector3(10,0,0)
    while not rl.window_should_close():
        rl.update_camera(cam, rl.CAMERA_THIRD_PERSON)

        rl.set_mouse_position(400, 300)

        # light
        cameraPos = [cam.position.x, cam.position.y, cam.position.z]
        rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], cameraPos, rl.SHADER_UNIFORM_VEC3)

        rlight.update_light_values(shader, sun)
        # lightend

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(cam)
        rl.begin_shader_mode(shader)

        opo = rl.vector3_rotate_by_axis_angle(opo, rl.Vector3(1, 1, 0), 0.1)
        rl.draw_cube_v(opo, rl.vector3_one, rl.RED)

        rl.draw_grid(100, 1)

        rl.draw_sphere(sun.position, 1, rl.GRAY)

        rl.end_shader_mode()
        rl.end_mode_3d()

        rl.end_drawing()

    rl.close_window()

#rottest()
animaltest()
