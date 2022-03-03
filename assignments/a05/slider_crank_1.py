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
## Slider-crank Chrono tutorial (model 1)
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
## The simulation is animated with Irrlicht.
##
## =============================================================================

from numpy import pi
import pychrono as chrono
from pychrono import irrlicht as chronoirr
from pychrono.core import ChLinkLockSpherical, ChLinkUniversal
import matplotlib.pyplot as plt
import time

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

cyl_g = chrono.ChCylinderShape();
cyl_g.GetCylinderGeometry().p1 = chrono.ChVectorD(0, 0.2, 0)
cyl_g.GetCylinderGeometry().p2 = chrono.ChVectorD(0, -0.2, 0)
cyl_g.GetCylinderGeometry().rad = 0.03
ground.AddAsset(cyl_g);

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

col_s = chrono.ChColorAsset()
col_s.SetColor(chrono.ChColor(0.2, 0.2, 0.6))
slider.AddAsset(col_s)

  #### -------------------------------------------------------------------------
  #### EXERCISE 1.1
  #### Create a connecting rod body to replace the distance constraint.
  #### This body should have:
  ####    mass: 0.5
  ####    moments of inertia:  I_xx = 0.005, I_yy = 0.1, I_zz = 0.1
  ####    visualization: a green box with width and height 0.1
  #### -------------------------------------------------------------------------

# Rod
rod = chrono.ChBody()
system.AddBody(rod)
rod.SetIdentifier(3)
rod.SetMass(0.5)
rod.SetName("rod")
rod.SetInertiaXX(chrono.ChVectorD(0.005, 0.1, 0.1))
rod.SetPos(chrono.ChVectorD(0, 0, 0))
rod.SetRot(chrono.ChQuaternionD(1, 0, 0, 0))

box_r = chrono.ChBoxShape()
box_r.GetBoxGeometry().Size = chrono.ChVectorD(2, 0.05, 0.05) #width and height
rod.AddAsset(box_r)

cyl_r = chrono.ChCylinderShape()
cyl_r.GetCylinderGeometry().p1 = chrono.ChVectorD(2, 0, 0.2)
cyl_r.GetCylinderGeometry().p2 = chrono.ChVectorD(2, 0, -0.2)
cyl_r.GetCylinderGeometry().rad = 0.03
rod.AddAsset(cyl_r)


col_r = chrono.ChColorAsset()       
col_r.SetColor(chrono.ChColor(0.2, 0.6, 0.2)) #set color to green
rod.AddAsset(col_r)



## 3. Create joint constraints.
##    All joint frames are specified in the global frame.

## Define two quaternions representing:
## - a rotation of -90 degrees around x (z2y) #z2x and z2y and chrono.Qunit
## - a rotation of +90 degrees around y (z2x)
z2y = chrono.Q_from_AngX(-chrono.CH_C_PI / 2)
z2x = chrono.Q_from_AngY(chrono.CH_C_PI / 2)

  #### -------------------------------------------------------------------------
  #### EXERCISE 1.2
  #### Replace the revolute joint between ground and crank with a
  #### ChLinkMotorRotationSpeed element and enforce constant angular speed of
  #### 180 degrees/s.
  #### -------------------------------------------------------------------------

#motor
motor = chrono.ChLinkMotorRotationSpeed()
motor.SetName("motor")
motor.Initialize(ground, crank, chrono.ChFrameD(chrono.ChVectorD(0, 0, 0), z2y))
motor_speed = chrono.ChFunction_Const(chrono.CH_C_PI) 
motor.SetSpeedFunction(motor_speed)
system.AddLink(motor)



## Prismatic joint between ground and slider.
## The translational axis of a prismatic joint is along the Z axis of the
## specified joint coordinate system.  Here, we apply the 'z2x' rotation to
## align it with the X axis of the global reference frame.
prismatic_ground_slider = chrono.ChLinkLockPrismatic()
prismatic_ground_slider.SetName("prismatic_ground_slider")
prismatic_ground_slider.Initialize(ground, slider, chrono.ChCoordsysD(chrono.ChVectorD(2, 0, 0), z2x))
system.AddLink(prismatic_ground_slider)

  #### -------------------------------------------------------------------------
  #### EXERCISE 1.3
  #### Replace the distance constraint with joints connecting the rod to the
  #### crank (use ChLinkLockSpherical) and to the slider (ChLinkUniversal). The
  #### universal joint's cross should be aligned with the Z and Y global axes.
  #### -------------------------------------------------------------------------
spherical_joint = chrono.ChLinkLockSpherical()
spherical_joint.SetName("spherical_joint")
spherical_joint.Initialize(crank, rod, chrono.ChCoordsysD(chrono.ChVectorD(-2, 0, 0), chrono.QUNIT)) 
system.AddLink(spherical_joint)

universal_joint = chrono.ChLinkUniversal()
universal_joint.SetName("universal_joint")
universal_joint.Initialize(rod, slider, chrono.ChFrameD(chrono.ChVectorD(2, 0, 0), z2x))
system.AddLink(universal_joint)


## 4. Write the system hierarchy to the console (default log output destination)
system.ShowHierarchy(chrono.GetLog())


## 5. Prepare visualization with Irrlicht
##    Note that Irrlicht uses left-handed frames with Y up.

## Create the Irrlicht application and set-up the camera.
application = chronoirr.ChIrrApp (
        system,                               ## pointer to the mechanical system
        "Slider-Crank Exercise 1",            ## title of the Irrlicht window
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

    #stopping the simulation after 4 seconds
    if(int(system.GetChTime()) == 4):
      break
    

    ## Finalize the graphical scene.
    application.EndScene()

    v = slider.GetPos()
    
    # for i in range(current_sim_time, current_sim_time + 4):
    times.append(time.time() - start)
    pos.append(v.x)
    

   

   

plt.plot(times, pos)
plt.title("Position of slider wrt to time")
plt.xlabel("Time in seconds")
plt.ylabel("Position of slider")
plt.show()