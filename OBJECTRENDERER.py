import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()
display = (1000, 1000)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Set up OpenGL perspective projection
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)  # Move the scene back a bit so we can see it

# Define cube vertices and surfaces
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# Define global variables to store rotation and translation values
rotation_x = 0
rotation_y = 0
rotation_z = 0
translation_x = 0
translation_y = 0
translation_z = 0

def handle_keyboard_input(key):
    global rotation_x, rotation_y, rotation_z, translation_x, translation_y, translation_z
    if key == pygame.K_LEFT:
        rotation_y += 5
    elif key == pygame.K_RIGHT:
        rotation_y -= 5
    elif key == pygame.K_UP:
        rotation_x += 5
    elif key == pygame.K_DOWN:
        rotation_x -= 5
    elif key == pygame.K_w:
        translation_z += 0.1
    elif key == pygame.K_s:
        translation_z -= 0.1
    elif key == pygame.K_a:
        translation_x -= 0.1
    elif key == pygame.K_d:
        translation_x += 0.1
    elif key == pygame.K_q:
        translation_y += 0.1
    elif key == pygame.K_e:
        translation_y -= 0.1

def handle_mouse_input(button):
    global translation_x, translation_y, translation_z, dragging, drag_start
    if button == 1:  # Left mouse button
        # Start dragging
        dragging = True
        drag_start = pygame.mouse.get_pos()
    elif button == 4:  # Scroll up
        translation_z += 0.1
    elif button == 5:  # Scroll down
        translation_z -= 0.1

# Define global variables
dragging = False
drag_start = (0, 0)
translation_x = 0
translation_y = 0
translation_z = 0

# Define shadow vertices (scaled down version of cube)
shadow_vertices = tuple((v[0]*0.5, -1, v[2]*0.5) for v in vertices)

# Define cube color and shadow color
cube_color = (0.7, 0.2, 0.2)
shadow_color = (0.2, 0.2, 0.2)
edge_color = (1.0, 1.0, 1.0)

# Define a cube rendering function
def draw_cube():
    glColor3fv(cube_color)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glColor3fv(edge_color)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Define shadow rendering function
def draw_shadow():
    glColor3fv(shadow_color)
    glBegin(GL_QUADS)
    for vertex in shadow_vertices:
        glVertex3fv(vertex)
    glEnd()

# Main application loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            handle_keyboard_input(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_input(event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                # Stop dragging
                dragging = False

    if dragging:
        # Calculate mouse movement
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - drag_start[0]
        dy = mouse_pos[1] - drag_start[1]
        # Adjust translation values based on mouse movement
        translation_x += dx * 0.01
        translation_y -= dy * 0.01
        # Update drag start position
        drag_start = mouse_pos

    # Clear the screen and set the color
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.2, 0.2, 0.2, 1.0)

    # Apply rotation and translation transformations
    glLoadIdentity()  # Reset transformation matrix
    glTranslatef(translation_x, translation_y, translation_z)
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)
    glRotatef(rotation_z, 0, 0, 1)

    # Draw the cube
    draw_cube()

    # Apply translation transformations for the shadow
    glTranslatef(0, -2, 0)  # Move the shadow down to the floor
    glDisable(GL_LIGHTING)  # Disable lighting for the shadow
    draw_shadow()  # Draw the shadow
    glEnable(GL_LIGHTING)  # Re-enable lighting

    # Update display
    pygame.display.flip()
    pygame.time.wait(10)
