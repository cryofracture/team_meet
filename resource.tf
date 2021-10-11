terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.15.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Pulls the image
resource "docker_image" "python" {
  name = "python:3-9"
  build {
    path = "."
    
    tag  = ["latest:dev"]
      
    # build_arg = {
    #   foo : "zoo"
    # }
    label = {
      author : "Cryofracture"
    }
  }
}

# Pulls the image
resource "docker_image" "mongodb" {
  name = "mongodb:latest"
  build {
    path = "."
    
    tag  = ["latest:dev"]
      
    # build_arg = {
    #   foo : "zoo"
    # }
    label = {
      author : "Cryofracture"
    }
  }
}

# Create a container
resource "docker_container" "dock_schedule" {
  image = docker_image.python.latest
  name  = "pyscheduler container"
}

# Create a container
resource "docker_container" "dock_mongo" {
  image = docker_image.mongodb.latest
  name  = "mongodb container"
}