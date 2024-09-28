provider "aws" {
  region = "us-east-1"
}
terraform {
  backend "s3" {
    bucket = "terraform-backend-practice-bucket1"
    key    = "Project/terraform.tfstate"
    region = "us-east-1"
  }
}
resource "aws_instance" "Project" {
    instance_type = "t2.micro"
    vpc_security_group_ids = [ "sg-0315170f9b2efb5a0" ]
    ami = "ami-0e86e20dae9224db8"
    subnet_id = "subnet-0a7b5d28324f6a9e1"
    key_name = "New_key2"
    tags = {
        Name = "practice"
    }
}
