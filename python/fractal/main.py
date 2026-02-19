import glfw
import moderngl
import numpy as np

WIDTH, HEIGHT = 1000, 800

# Mandelbrot shader (runs on GPU)
fragment_shader = """
#version 330

uniform vec2 resolution;
uniform vec2 center;
uniform float zoom;
uniform int max_iter;

out vec4 fragColor;

void main() {
    vec2 uv = (gl_FragCoord.xy / resolution - 0.5) * 2.0;
    float aspect = resolution.x / resolution.y;
    uv.x *= aspect;

    vec2 c = center + uv / zoom;
    vec2 z = vec2(0.0);

    int i;
    for(i = 0; i < max_iter; i++) {
        if(dot(z, z) > 4.0) break;
        z = vec2(
            z.x*z.x - z.y*z.y + c.x,
            2.0*z.x*z.y + c.y
        );
    }

    float t = float(i) / float(max_iter);
    fragColor = vec4(t, sqrt(t), 1.0 - t, 1.0);
}
"""

if not glfw.init():
    raise Exception("GLFW init failed")

window = glfw.create_window(WIDTH, HEIGHT, "GPU Mandelbrot", None, None)
glfw.make_context_current(window)

ctx = moderngl.create_context()

prog = ctx.program(
    vertex_shader="""
        #version 330
        in vec2 in_pos;
        void main() {
            gl_Position = vec4(in_pos, 0.0, 1.0);
        }
    """,
    fragment_shader=fragment_shader,
)

quad = ctx.buffer(np.array([
    -1.0, -1.0,
     1.0, -1.0,
    -1.0,  1.0,
     1.0,  1.0,
], dtype='f4'))

vao = ctx.simple_vertex_array(prog, quad, 'in_pos')

center = [ -0.5, 0.0 ]
zoom = 1.0
max_iter = 200

while not glfw.window_should_close(window):
    glfw.poll_events()

    # Zoom
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        zoom *= 1.02
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        zoom /= 1.02

    # Move
    speed = 0.01 / zoom
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        center[1] += speed
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        center[1] -= speed
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        center[0] -= speed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        center[0] += speed

    ctx.clear()
    prog['resolution'].value = (WIDTH, HEIGHT)
    prog['center'].value = tuple(center)
    prog['zoom'].value = zoom
    prog['max_iter'].value = max_iter

    vao.render(moderngl.TRIANGLE_STRIP)
    glfw.swap_buffers(window)

glfw.terminate()
