#!/bin/bash
# Set Bedrock model environment variables

# BASE_MODEL: For text-only operations (Generate, RefineA)
# Use efficient Nova Lite for fast, cost-effective text generation
export BASE_MODEL="us.amazon.nova-lite-v1:0"

# VLM_MODEL: For vision operations (Caption, RefineB, InspireA)  
export VLM_MODEL="us.amazon.nova-2-lite-v1:0"

echo "Environment variables set:"
echo "  BASE_MODEL=$BASE_MODEL"
echo "  VLM_MODEL=$VLM_MODEL"
echo ""
echo "Usage: source set_models.sh"
