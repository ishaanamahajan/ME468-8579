## =============================================================================
## PROJECT CHRONO - http:##projectchrono.org
##
## Copyright (c) 2014 projectchrono.org
## All right reserved.
##
## Use of this source code is governed by a BSD-style license that can be found
## in the LICENSE file at the top level of the distribution and at
## http://projectchrono.org/license-chrono.txt.
##
## =============================================================================
## Author: Simone Benatti
## =============================================================================
##
## Slider-crank Chrono tutorial (model 2)
##
## This model is a 3-body slider-crank consisting of crank, slider and connecting
## rod bodies. The crank is connected to ground with a revolute joint and the
## slider is connected to ground through a prismatic joint.  The connecting rod
## connects to the crank through a spherical joint and to the slider through a
## universal joint.
##
## The crank body is driven at constant angular speed, under the action of gravity,
## acting in the negative Z direction.
##
## An additional spherical body, constrained to move along the global X axis
## through a prismatic joint and connected to ground with a translational spring
## damper, interacts through contact with the slider body.
##
## The simulation is animated with Irrlicht.
##
## =============================================================================

import pychrono as chrono
from pychrono import irrlicht as chronoirr
import time
import matplotlib.pyplot as plt


## 0. Set the path to the Chrono data folder
chrono.SetChronoDataPath('C:/codes/Chrono/Chrono_Source/data/')

## 1. Create the physical system that will handle all bodies and constraints.

##    Specify the gravitational acceleration vector, consistent with the
##    global reference frame having Z up.
system = chrono.ChSystemNSC()
system.Set_G_acc(chrono.ChVectorD(0, 0, -9.81))

## 2. Create the rigid bodies of the slider-crank mechanical system.
##    For each body, specify:
##    - a unique identifier
##    - mass and moments of inertia
##    - position and orientation of the (centroidal) body frame
##    - visualization assets (defined with respect to the body frame)

## Ground
ground = chrono.ChBody()
system.AddBody(ground)
ground.SetIdentifier(-1)
ground.SetName("ground")
ground.SetBodyFixed(True)

cyl_g = chrono.ChCylinderShape()
cyl_g.GetCylinderGeometry().p1 = chrono.ChVectorD(0, 0.2, 0)
cyl_g.GetCylinderGeometry().p2 = chrono.ChVectorD(0, -0.2, 0)
cyl_g.GetCylinderGeometry().rad = 0.03
ground.AddAsset(cyl_g)

col_g = chrono.ChColorAsset()
col_g.SetColor(chrono.ChColor(0.6, 0.6, 0.2))
ground.AddAsset(col_g)

## Crank
crank = chrono.ChBody()
system.AddBody(crank)
crank.SetIdentifier(1)
crank.SetName("crank")
crank.SetMass(1.0)
crank.SetInertiaXX(chrono.ChVectorD(0.005, 0.1, 0.1))
crank.SetPos(chrono.ChVectorD(-1, 0, 0))
crank.SetRot(chrono.ChQuaternionD(1, 0, 0, 0))

box_c = chrono.ChBoxShape()
box_c.GetBoxGeometry().Size = chrono.ChVectorD(0.95, 0.05, 0.05)
crank.AddAsset(box_c)

cyl_c = chrono.ChCylinderShape()
cyl_c.GetCylinderGeometry().p1 = chrono.ChVectorD(1, 0.1, 0)
cyl_c.GetCylinderGeometry().p2 = chrono.ChVectorD(1, -0.1, 0)
cyl_c.GetCylinderGeometry().rad = 0.05
crank.AddAsset(cyl_c)

sph_c = chrono.ChSphereShape()
sph_c.GetSphereGeometry().center = chrono.ChVectorD(-1, 0, 0)
sph_c.GetSphereGeometry().rad = 0.05
crank.AddAsset(sph_c)

col_c = chrono.ChColorAsset()
col_c.SetColor(chrono.ChColor(0.6, 0.2, 0.2))
crank.AddAsset(col_c)

## Slider
slider = chrono.ChBody()
system.AddBody(slider)
slider.SetIdentifier(2)
slider.SetName("slider")
slider.SetMass(1.0)
slider.SetInertiaXX(chrono.ChVectorD(0.05, 0.05, 0.05))
slider.SetPos(chrono.ChVectorD(2, 0, 0))
slider.SetRot(chrono.ChQuaternionD(1, 0, 0, 0))

box_s = chrono.ChBoxShape()
box_s.GetBoxGeometry().Size = chrono.ChVectorD(0.2, 0.1, 0.1)
slider.AddAsset(box_s)

cyl_s = chrono.ChCylinderShape()
cyl_s.GetCylinderGeometry().p1 = chrono.ChVectorD(0, 0.2, 0)
cyl_s.GetCylinderGeometry().p2 = chrono.ChVectorD(0, -0.2, 0)
cyl_s.GetCylinderGeometry().rad = 0.03
slider.AddAsset(cyl_s)

col_s = chrono.ChColorAsset()
col_s.SetColor(chrono.ChColor(0.2, 0.2, 0.6))
slider.AddAsset(col_s)

## Connecting rod
rod = chrono.ChBody()
system.AddBody(rod)
rod.SetIdentifier(3)
rod.SetName("rod")
rod.SetMass(0.5)
rod.SetInertiaXX(chrono.ChVectorD(0.005, 0.1, 0.1))
rod.SetPos(chrono.ChVectorD(0, 0, 0))
rod.SetRot(chrono.ChQuaternionD(1, 0, 0, 0))

box_r = chrono.ChBoxShape()
box_r.GetBoxGeometry().Size = chrono.ChVectorD(2, 0.05, 0.05)
rod.AddAsset(box_r)

cyl_r = chrono.ChCylinderShape()
cyl_r.GetCylinderGeometry().p1 = chrono.ChVectorD(2, 0, 0.2)
cyl_r.GetCylinderGeometry().p2 = chrono.ChVectorD(2, 0, -0.2)
cyl_r.GetCylinderGeometry().rad = 0.03
rod.AddAsset(cyl_r)

col_r = chrono.ChColorAsset()
col_r.SetColor(chrono.ChColor(0.2, 0.6, 0.2))
rod.AddAsset(col_r)

  #### -------------------------------------------------------------------------
  #### EXERCISE 2.1
  #### Enable contact on the slider body and specify contact geometry
  #### The contact shape attached to the slider body should be a box with the
  #### same dimensions as the visualization asset, centered at the body origin.
  #### Use a coefficient of friction of 0.4.
  #### -------------------------------------------------------------------------
  
slider.SetCollide(True)
slider_mat = chrono.ChMaterialSurfaceNSC()
slider_mat.SetFriction(0.4)

slider.GetCollisionModel().ClearModel()
slider.GetCollisionModel().AddBox(slider_mat, 0.2, 0.1, 0.1, chrono.VNULL, chrono.ChMatrix33D(chrono.QUNIT))
slider.GetCollisionModel().BuildModel()
  





  #### -------------------------------------------------------------------------
  #### EXERCISE 2.2
  #### Create a new body, with a spherical shape (radius 0.2), used both as
  #### visualization asset and contact shape (mu = 0.4). This body should have:
  ####    mass: 1
  ####    moments of inertia: I_xx = I_yy = I_zz = 0.02
  ####    initial location: (5.5, 0, 0)
  #### -------------------------------------------------------------------------
sphere = chrono.ChBody()
system.AddBody(sphere)
sphere.SetIdentifier(4)
sphere.SetName("sphere")
sphere.SetMass(1)
sphere.SetInertiaXX(chrono.ChVectorD(0.02, 0.02, 0.02))
sphere.SetPos(chrono.ChVectorD(5.5, 0, 0))
sphere.SetRot(chrono.ChQuaternionD(1, 0, 0, 0))

sphere.SetCollide(True)
sphere_mat = chrono.ChMaterialSurfaceNSC()

sphere.GetCollisionModel().ClearModel()
sphere.GetCollisionModel().AddSphere(sphere_mat, 0.2, chrono.ChVectorD(0, 0, 0))
sphere.GetCollisionModel().BuildModel()
  

sphere0 = chrono.ChSphereShape()
sphere0.GetSphereGeometry().rad = 0.2
sphere0.GetSphereGeometry().center = chrono.ChVectorD(0, 0, 0)
sphere.AddAsset(sphere0)


## 3. Create joint constraints.
##    All joint frames are specified in the global frame.

## Define two quaternions representing:
## - a rotation of -90 degrees around x (z2y)
## - a rotation of +90 degrees around y (z2x)
z2y = chrono.Q_from_AngX(-chrono.CH_C_PI / 2)
z2x = chrono.Q_from_AngY(chrono.CH_C_PI / 2)

## Create a ChFunction object that always returns the constant value PI.
fun = chrono.ChFunction_Const()
fun.Set_yconst(chrono.CH_C_PI)

## Motor between ground and crank.
## Note that this also acts as a revolute joint (i.e. it enforces the same
## kinematic constraints as a revolute joint).  As before, we apply the 'z2y'
## rotation to align the rotation axis with the Y axis of the global frame.
engine_ground_crank = chrono.ChLinkMotorRotationSpeed()
engine_ground_crank.SetName("engine_ground_crank")
engine_ground_crank.Initialize(ground, crank, chrono.ChFrameD(chrono.ChVectorD(0, 0, 0), z2y))
engine_ground_crank.SetSpeedFunction(fun)
system.AddLink(engine_ground_crank)

## Prismatic joint between ground and slider.
## The translational axis of a prismatic joint is along the Z axis of the
## specified joint coordinate system.  Here, we apply the 'z2x' rotation to
## align it with the X axis of the global reference frame.
prismatic_ground_slider = chrono.ChLinkLockPrismatic()
prismatic_ground_slider.SetName("prismatic_ground_slider")
prismatic_ground_slider.Initialize(ground, slider, chrono.ChCoordsysD(chrono.ChVectorD(2, 0, 0), z2x))
system.AddLink(prismatic_ground_slider)

## Spherical joint between crank and rod
spherical_crank_rod = chrono.ChLinkLockSpherical()
spherical_crank_rod.SetName("spherical_crank_rod")
spherical_crank_rod.Initialize(crank, rod, chrono.ChCoordsysD(chrono.ChVectorD(-2, 0, 0), chrono.QUNIT))
system.AddLink(spherical_crank_rod)

## Universal joint between rod and slider.
## The "cross" of a universal joint is defined using the X and Y axes of the
## specified joint coordinate frame. Here, we apply the 'z2x' rotation so that
## the cross is aligned with the Z and Y axes of the global reference frame.
universal_rod_slider = chrono.ChLinkUniversal()
universal_rod_slider.SetName("universal_rod_slider")
universal_rod_slider.Initialize(rod, slider, chrono.ChFrameD(chrono.ChVectorD(2, 0, 0), z2x))
system.AddLink(universal_rod_slider)

  #### -------------------------------------------------------------------------
  #### EXERCISE 2.3
  #### Add a prismatic joint between ground and ball to constrain the ball's
  #### motion to the global X axis.
  #### -------------------------------------------------------------------------

prismatic_ground_ball = chrono.ChLinkLockPrismatic()
prismatic_ground_ball.SetName("prismatic_ground_ball")
prismatic_ground_ball.Initialize(ground, sphere, chrono.ChCoordsysD(chrono.ChVectorD(5.5, 0, 0), z2x))
system.AddLink(prismatic_ground_ball)


  #### -------------------------------------------------------------------------
  #### EXERCISE 2.4
  #### Add a spring-damper (ChLinkTSDA) between ground and the ball.
  #### This element should connect the center of the ball with the global point
  #### (6.5, 0, 0).  Set a spring constant of 50 and a spring free length of 1.
  #### Set a damping coefficient of 5.
  #### -------------------------------------------------------------------------

spring_damper = chrono.ChLinkTSDA()
spring_damper.SetName("spring_damper")
spring_damper.Initialize(ground, sphere, False, chrono.ChVectorD(6.5, 0, 0), chrono.ChVectorD(5.5, 0, 0))
spring_damper.SetSpringCoefficient(50.0)
spring_damper.SetDampingCoefficient(5.0)
spring_damper.SetRestLength(1.0)

spring_tsda = chrono.ChPointPointSpring(0.05, 80, 15)
spring_damper.AddAsset(spring_tsda)

col_tsda = chrono.ChColorAsset()
col_tsda.SetColor(chrono.ChColor(0.6, 0.2, 0.2))
spring_damper.AddAsset(col_tsda)

system.AddLink(spring_damper)


## 4. Write the system hierarchy to the console (default log output destination)
system.ShowHierarchy(chrono.GetLog())

## 5. Prepare visualization with Irrlicht
##    Note that Irrlicht uses left-handed frames with Y up.

## Create the Irrlicht application and set-up the camera.
application = chronoirr.ChIrrApp (
        system,                               ## pointer to the mechanical system
        "Slider-Crank Exercise 2",            ## title of the Irrlicht window
        chronoirr.dimension2du(800, 600),     ## window dimension (width x height)
        chronoirr.VerticalDir_Z)              ## up direction
application.AddTypicalLights()
application.AddCamera(
        chronoirr.vector3df(2, -5, 0),        ## camera location
        chronoirr.vector3df(2, 0, 0))         ## "look at" location

## Let the Irrlicht application convert the visualization assets.
application.AssetBindAll()
application.AssetUpdateAll()

## 6. Perform the simulation.

## Specify the step-size.
application.SetTimestep(0.01)
application.SetTryRealtime(True)


times = []
pos = []
t = []
#current_sim_time = int (system.GetChTime())
start = time.time()
while (application.GetDevice().run()):
    ## Initialize the graphical scene.
    application.BeginScene(True, True, chronoirr.SColor(255, 225, 225, 225))
    
    ## Render all visualization objects.
    application.DrawAll()

    ## Draw an XZ grid at the global origin to add in visualization. 
    chronoirr.drawGrid(
        application.GetVideoDriver(), 1, 1, 20, 20,
        chrono.ChCoordsysD(chrono.ChVectorD(0, 0, 0), chrono.Q_from_AngX(chrono.CH_C_PI_2)),
        chronoirr.SColor(255, 80, 100, 100), True)
    chronoirr.drawAllCOGs(system, application.GetVideoDriver(), 1)

    ## Advance simulation by one step.
    application.DoStep()

    if(int(system.GetChTime()) == 4):
      break
   
    # getting the torque value
    torque = engine_ground_crank.GetMotorTorque()

    ## Finalize the graphical scene.
    application.EndScene()

    v = slider.GetPos()
    
    # for i in range(current_sim_time, current_sim_time + 4):
    times.append(time.time() - start)
    pos.append(v.x)
    t.append(torque)

    
plt.plot(times, pos)
plt.title("Position of slider wrt to time")
plt.xlabel("Time in seconds")
plt.ylabel("Position of slider")
plt.plot(times, torque)
plt.show()
