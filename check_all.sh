#!/bin/bash
echo "Checking code convention compliance..."
pycodestyle trolog/* tests/*
if [ $? -eq 0 ]; then
    echo "Running unit tests..."
    pytest tests
fi
