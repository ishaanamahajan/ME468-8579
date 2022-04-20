#!/usr/bin/env bash

ls /home &> $HOME/home.out
hostname &> $HOME/hostname.out
nvidia-smi &> $HOME/nvidia.out
ros2 &> $HOME/ros2.out
python3 demo_SEN_camera.py &> $HOME/script.out
