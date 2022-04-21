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
## Author: Radu Serban
## =============================================================================
##
## Wheeled vehicle tutorial
##
## =============================================================================

import pychrono as chrono
import pychrono.vehicle as veh
import pychrono.irrlicht as chronoirr
import os
import math as m

## -----------------------------------------------------------------------------

# Function to add falling objects
def AddMovingObstacles(system) :
    # Create contact material, of appropriate type. Use default properties
    material = None
    if (NSC_SMC == chrono.ChContactMethod_NSC) :
        matNSC = chrono.ChMaterialSurfaceNSC()
        #Change NSC material properties as desired
        material = matNSC
    elif (NSC_SMC == chrono.ChContactMethod_SMC) :
        matSMC = chrono.ChMaterialSurfaceSMC()
        # Change SMC material properties as desired
        material = matSMC
    else:
        raise("Invalid Contact Method")
    sizeX = 300
    sizeY = 300
    height = 0
    numObstacles = 10

    for i in range(numObstacles) :
        o_sizeX = 1.0 + 3.0 * chrono.ChRandom()
        o_sizeY = 0.3 + 0.2 * chrono.ChRandom()
        o_sizeZ = 0.05 + 0.1 * chrono.ChRandom()
        obstacle = chrono.ChBodyEasyBox(o_sizeX, o_sizeY, o_sizeZ, 2000.0, True, True, material)

        o_posX = (chrono.ChRandom() - 0.5) * 0.4 * sizeX
        o_posY = (chrono.ChRandom() - 0.5) * 0.4 * sizeY
        o_posZ = height + 4
        rot = chrono.ChQuaternionD(chrono.ChRandom(), chrono.ChRandom(), chrono.ChRandom(), chrono.ChRandom())
        rot.Normalize()
        obstacle.SetPos(chrono.ChVectorD(o_posX, o_posY, o_posZ))
        obstacle.SetRot(rot)

        system.AddBody(obstacle)
    
## -----------------------------------------------------------------------------

# Function to add obstacles
def AddFixedObstacles(system) :
    # Create contact material, of appropriate type. Use default properties
    material = None
    if (NSC_SMC == chrono.ChContactMethod_NSC) :
        matNSC = chrono.ChMaterialSurfaceNSC()
        #Change NSC material properties as desired
        material = matNSC
    elif (NSC_SMC == chrono.ChContactMethod_SMC) :
        matSMC = chrono.ChMaterialSurfaceSMC()
        # Change SMC material properties as desired
        material = matSMC
    else:
        raise("Invalid Contact Method")

    for i in range(8) :
        obstacle = chrono.ChBodyEasyCylinder(0.5, 6.0, 2000, True, True, material)
        obstacle.SetPos(chrono.ChVectorD(-2.0 * i + 20, 0, -0.4))
        
        obstacle.SetRot(chrono.Q_from_AngAxis(15 * chrono.CH_C_DEG_TO_RAD, chrono.VECT_Y))
        obstacle.SetBodyFixed(True);
        system.AddBody(obstacle);
        
## =============================================================================

# JSON-specification files for vehicle system and subsystems

vehicle_file = "vehicle/WheeledVehicle.json"
rigidtire_file = "vehicle/RigidTire.json"
simplepowertrain_file = "vehicle/SimplePowertrain.json"
rigidterrain_file = "terrain/RigidPlane.json"

# Initial vehicle position and orientation
initLoc = chrono.ChVectorD(0, 0, 1.0)
initRot = chrono.ChQuaternionD(1, 0, 0, 0)

# Simulation step size
step_size = 1e-3

# Time interval between two render frames
render_step_size = 1.0 / 50    # FPS = 50

# Point on chassis tracked by the camera
trackPoint = chrono.ChVectorD(0.0, 0.0, 1.75)

# Contact method
NSC_SMC = chrono.ChContactMethod_SMC


# ----------------------
# Set path to data files
# ----------------------

# Path to Chrono data files (textures, fonts, etc.)
chrono.SetChronoDataPath("./data/")

# Path to the data files for this vehicle (JSON specification files)
veh.SetDataPath("./data/")

# --------------------------
# Create the various modules
# --------------------------
    
# Create and initialize the vehicle system
vehicle = veh.WheeledVehicle(veh.GetDataFile(vehicle_file), NSC_SMC)

vehicle.Initialize(chrono.ChCoordsysD(initLoc, initRot))

vehicle.SetSuspensionVisualizationType(veh.VisualizationType_PRIMITIVES)
vehicle.SetSteeringVisualizationType(veh.VisualizationType_PRIMITIVES)
vehicle.SetWheelVisualizationType(veh.VisualizationType_NONE)

# Create the terrain
terrain = veh.RigidTerrain(vehicle.GetSystem(), veh.GetDataFile(rigidterrain_file))
AddFixedObstacles(vehicle.GetSystem())
##AddMovingObstacles(vehicle.GetSystem())

# Create and initialize the powertrain system
powertrain = veh.SimplePowertrain(veh.GetDataFile(simplepowertrain_file))
vehicle.InitializePowertrain(powertrain)

# Create and initialize the tires
for axle in vehicle.GetAxles() :
    tireL = veh.RigidTire(veh.GetDataFile(rigidtire_file))
    tireR = veh.RigidTire(veh.GetDataFile(rigidtire_file))
    vehicle.InitializeTire(tireL, axle.m_wheels[0], veh.VisualizationType_MESH)
    vehicle.InitializeTire(tireR, axle.m_wheels[1], veh.VisualizationType_MESH)
    
# Create the Irrlicht vehicle application
app = veh.ChVehicleIrrApp(vehicle, "Vehicle Demo")

app.AddTypicalLights()
app.SetChaseCamera(trackPoint, 6.0, 0.5)

app.SetTimestep(step_size)

app.AssetBindAll()
app.AssetUpdateAll()

# Create the driver system (interactive)
driver = veh.ChIrrGuiDriver(app)

# Set the time response for steering and throttle keyboard inputs.
# NOTE: this is not exact, since we do not render quite at the specified FPS.
steering_time = 1.0;  # time to go from 0 to +1 (or from 0 to -1)
throttle_time = 1.0;  # time to go from 0 to +1
braking_time = 0.3;   # time to go from 0 to +1
driver.SetSteeringDelta(render_step_size / steering_time)
driver.SetThrottleDelta(render_step_size / throttle_time)
driver.SetBrakingDelta(render_step_size / braking_time)

# ---------------
# Simulation loop
# ---------------

# Number of simulation steps between two 3D view render frames
render_steps = m.ceil(render_step_size / step_size)

#Initialize simulation frame counter and simulation time
step_number = 0
time = 0

realtime_timer = chrono.ChRealtimeStepTimer()

while (app.GetDevice().run())  :
    # Render scene
    if (step_number % render_steps == 0) :
        app.BeginScene(True, True, chronoirr.SColor(255, 140, 161, 192))
        app.DrawAll();
        app.EndScene();
        
    # Get driver inputs
    driver_inputs = driver.GetInputs()

    # Update modules (process inputs from other modules)
    time = vehicle.GetSystem().GetChTime()
    driver.Synchronize(time)
    vehicle.Synchronize(time, driver_inputs, terrain)
    terrain.Synchronize(time)
    app.Synchronize("", driver_inputs)

    # Advance simulation for one timestep for all modules
    driver.Advance(step_size)
    vehicle.Advance(step_size)
    terrain.Advance(step_size)
    app.Advance(step_size)


    # Increment step number
    step_number += 1
    # Spin in place for real time to catch up
    realtime_timer.Spin(step_size)