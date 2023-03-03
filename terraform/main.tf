terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = local.region
}

locals {
  region            = "us-east-1"
  availability_zone = "${local.region}a"
  vpc_id            = "vpc-aa592cd7"
  subnet_id         = "subnet-4af2ab2c"
  tags = {
    Name = "mtb-bike-compare-project"
  }
}

resource "aws_security_group" "not_open_to_world" {
  name        = "not_open_to_world"
  description = "SG for mtb-bike-compare project EC2 instance"
  vpc_id      = local.vpc_id

  ingress {
    description = "Allow all inbound access to mtb-bike-compare site"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Allow SSH inbound to mtb-bike-compare EC2"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["24.8.119.103/32"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = local.tags

}


resource "aws_instance" "mtb-bike-compare" {
  ami                         = "ami-0aa7d40eeae50c9a9"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
  security_groups             = [aws_security_group.not_open_to_world.id]
  subnet_id                   = local.subnet_id
  key_name                    = "mtb-bike-compare"

  ebs_block_device {
    device_name = "/dev/sdh"
    volume_size = 10
    volume_type = "standard"

    tags = local.tags
  }

  tags = local.tags
}

resource "aws_route53_zone" "bikesearcher" {
  name = "thebikesearcher.com"
}

resource "aws_route53_record" "a_record" {
  zone_id = aws_route53_zone.bikesearcher.zone_id
  name    = "thebikesearcher.com"
  type    = "A"
  ttl     = 300
  records = [aws_instance.mtb-bike-compare.public_ip]
}
