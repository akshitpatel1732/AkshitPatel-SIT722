variable "prefix" {
  description = "Prefix for all resource names"
  type        = string
  default     = "224579861week10prod"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "australiaeast"
}

variable "kubernetes_version" {
  default = "1.31.7"
}