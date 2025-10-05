terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "postgres" {
  name = "postgres:alpine"
}

resource "docker_volume" "pgdata" {}

resource "docker_container" "postgres" {
  image = docker_image.postgres.image_id
  name  = "postgres_local"
  ports {
    internal = var.porta_interna
    external = var.porta_externa
  }
  env = [
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_DB=${var.postgres_db}"
  ]
  volumes {
    container_path = "/var/lib/postgresql/data"
    volume_name    = docker_volume.pgdata.name
  }
  restart = "unless-stopped"
}

output "postgres_host" {
  value       = var.hostvar
  description = "Endereço do banco PostgreSQL criado"
}