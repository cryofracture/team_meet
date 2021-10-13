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
  name = "cryofracture/dock_schedule"
  build {
    path = "dock_schedule"
    
    tag  = ["latest:dev"]
      
    # build_arg = {
    #   foo : "zoo"
    # }
    label = {
      author : "cryofracture"
    }
  }
}

# Pulls the image
# resource "docker_image" "mongodb" {
#   name = "mongodb:latest"
#   build {
#     path = "."
    
#     tag  = ["latest:dev"]
      
#     # build_arg = {
#     #   foo : "zoo"
#     # }
#     label = {
#       author : "Cryofracture"
#     }
#   }
# }

# Create a container
resource "docker_container" "dock_schedule" {
  image = docker_image.python.latest
  name  = "dock_schedule"
}

# # Create a container
# resource "docker_container" "dock_mongo" {
#   image = docker_image.mongodb.latest
#   name  = "mongodb container"
# }

# Create a network for the app
resource "docker_network" "dock_schedule_network" {
  name = "dock_schedule"
  driver = "bridge"
  check_duplicate = true
  ingress = false
  attachable = true
}