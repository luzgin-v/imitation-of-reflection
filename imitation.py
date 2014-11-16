# -*- coding: utf-8 -*- 
import sys,time,random
from math import *
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from Image import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''
  sys.exit()
light_position =  [4.0,4.0,4.0, 0.0]
x_view = 0
y_view = 4
z_view = 5
x_rot = 0
y_rot = 0
z_rot = 0
texture = None
textures = {}
t0 = time.time()
frames = 0
fps= None
def framerate():
    global t0, frames,fps
    t = time.time()
    frames += 1
    if t - t0 >= 5.0:
        seconds = t - t0
        fps = frames/seconds
        fps = "%.0f frames in %3.1f seconds = %6.3f FPS" % (frames,seconds,fps)
        t0 = t
        frames = 0
        
def LoadTextures(fname):
	if textures.get( fname ) is not None:
		return textures.get( fname )
	texture = textures[fname] = glGenTextures(1)
	image = open(fname)
	ix = image.size[0]
	iy = image.size[1]
	image = image.tostring('raw', 'RGBX', 0, -1)
	# Create Texture    
	glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	return texture
  
def floor(scale, h, n, texture):
	glPushMatrix ()
	glTranslatef(0.0,h ,0.0)
	glScalef(scale,0.0 ,scale)
	glBindTexture(GL_TEXTURE_2D, texture)
	glBegin(GL_QUADS)
	glNormal3d(0, 1, 0)
	glTexCoord2f(0.0, 0.0)
	glVertex3d(-20.0,0.0 ,-20.0)
	glTexCoord2f(n, 0.0)
	glVertex3d(20.0,0.0 ,-20.0)
	glTexCoord2f(n, n)
	glVertex3d(20.0,0.0 ,20.0)
	glTexCoord2f(0.0, n)
	glVertex3d(-20.0,0.0 ,20.0)
	glEnd()
	glPopMatrix ()
	
def plane(scale, h):
	glPushMatrix ()
	glTranslatef(0.0,h ,0.0)
	glScalef(scale,0.0 ,scale)
	spec = [1.0, 1.0, 1.0, 1.0]
	glMaterialfv(GL_FRONT, GL_SPECULAR, spec)
	glMateriali(GL_FRONT, GL_SHININESS, 128)
	glBegin(GL_QUADS)
	glColor4f(0.7,0.7,1.0,0.5)
	glNormal3d(0, 1, 0)
	glVertex3d(-20.0,0.0 ,-20.0)
	glVertex3d(20.0,0.0 ,-20.0)
	glVertex3d(20.0,0.0 ,20.0)
	glVertex3d(-20.0,0.0 ,20.0)
	glEnd()
	glPopMatrix ()
	
def teapot(rad):
	glColor3f(0.69,0.74,0.85)
	glutSolidTeapot(rad)
	
def sphere(rad,color):
	glColor3f(0.69,0.74,0.85)
	glutSolidSphere (rad, rad*16, rad*16)
	
def init():
   global texture
   global light_position
   texture = LoadTextures('floor.bmp')
   # цвет очистки
   glClearColor (0.0, 0.0, 1.0, 0.0)
   glClearDepth(1.0)
   glClearStencil(0)
   # плавная закраска, если не требуется, то параметр - GL_FLAT
   glShadeModel (GL_SMOOTH)
   
   light_ambient =  [0.7,0.7,0.7, 1.0]
   light_diffuse =  [1.0,1.0,1.0, 1.0]
   light_specular =  [0,5, 0.5, 0.5, 1.0]
   glLightfv(GL_LIGHT0, GL_POSITION, light_position)
   glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
   glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
   glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
   glEnable(GL_LIGHTING)
   glEnable(GL_LIGHT0)
   glEnable(GL_DEPTH_TEST)
   glEnable(GL_NORMALIZE)

def display():
   global x_rot, y_rot, z_rot
   # очистка буферов цвета и глубины кадра
   glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
   
   #надписи
   glColor3d(1, 1, 1)
   glWindowPos2i(20, 580);
   glutBitmapString(GLUT_BITMAP_HELVETICA_12, 'Press left button to start and right button to stop');
   framerate()
   glWindowPos2i(20, 560)
   glutBitmapString(GLUT_BITMAP_HELVETICA_12, fps)
   
   # проекционная трансформация
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity() # инициализация матрицы
   gluPerspective(45, 4/3, 0.1, 100)
   gluLookAt (x_view, y_view, z_view, 0, 0, 0, 0, 1, 0) # (x,y,z - положение камеры; x,y,z - цель камеры; x,y,z - определение наклона камеры, верхнее направление)
   
   # модельные трансформации
   glMatrixMode(GL_MODELVIEW)
   glColorMask(0,0,0,0)
   glEnable(GL_STENCIL_TEST)
   glStencilFunc(GL_ALWAYS, 1, 1)
   glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
   glDisable(GL_DEPTH_TEST)
   plane(0.2, 0.0)
   
   glEnable(GL_DEPTH_TEST)
   glColorMask(1,1,1,1)
   glStencilFunc(GL_EQUAL, 1, 1)
   glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
   
   glEnable(GL_CLIP_PLANE0)
   glClipPlane(GL_CLIP_PLANE0, (0.0,-1.0, 0.0, 0.0))
   
   glPushMatrix()
   glScalef(1.0, -1.0, 1.0)
   glLightfv(GL_LIGHT0, GL_POSITION, light_position)
   glTranslatef(0.0, 1.6, 0.0)
   glRotatef(x_rot, 1.0, 0.0, 0.0)
   glRotatef(y_rot, 0.0, 1.0, 0.0)
   glRotatef(z_rot, 0.0, 0.0, 1.0)
   teapot(1)
   glPopMatrix()
   
   glDisable(GL_CLIP_PLANE0)
   glDisable(GL_STENCIL_TEST)
   
   glLightfv(GL_LIGHT0, GL_POSITION, light_position)
   glEnable(GL_BLEND)
   glDisable(GL_LIGHTING)
   glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   plane(0.2, 0.0)
   glEnable(GL_LIGHTING)
   glDisable(GL_BLEND)
   
   glPushMatrix()
   glTranslatef(0.0, 1.6, 0.0)
   glRotatef(x_rot, 1.0, 0.0, 0.0)
   glRotatef(y_rot, 0.0, 1.0, 0.0)
   glRotatef(z_rot, 0.0, 0.0, 1.0)
   teapot(1)
   glPopMatrix()
   
   #glFlush()
   glutSwapBuffers()
   
def rotate():
	global x_rot, y_rot, z_rot
	x_rot += 0.6
	y_rot += 0.6
	z_rot += 0.6
	if(x_rot > 360.0):
		x_rot = x_rot - 360.0
	if(y_rot > 360.0):
		y_rot = y_rot - 360.0
	if(z_rot > 360.0):
		z_rot = z_rot - 360.0
	glutPostRedisplay()

def keyboard(key, x, y):
   if key == chr(27):
       sys.exit(0) 

def mouse(button, state, x, y):
   if button == GLUT_LEFT_BUTTON:
       if(state == GLUT_DOWN):
          glutIdleFunc(rotate)
   elif button == GLUT_RIGHT_BUTTON:
       if(state == GLUT_DOWN):
           glutIdleFunc(None)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutInitWindowPosition(100, 100)
glutCreateWindow("imitation reflection")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutMainLoop()
