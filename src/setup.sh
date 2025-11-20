#!/bin/bash

# Aegis Intelligence Database - Quick Start Script
# This script helps set up and run the application

echo "=========================================="
echo "AEGIS INTELLIGENCE DATABASE - SETUP"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "❌ MySQL is not installed. Please install MySQL Server 8.0+."
    exit 1
fi

echo "✓ MySQL found"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Setup database
echo "🗄️  Setting up database..."
echo "Please enter your MySQL root password when prompted."
echo ""

read -p "Do you want to setup the database now? (y/n): " setup_db

if [ "$setup_db" = "y" ] || [ "$setup_db" = "Y" ]; then
    echo "Creating database..."
    mysql -u root -p < schema.sql
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create database schema"
        exit 1
    fi
    
    echo "Populating database..."
    mysql -u root -p < populate.sql
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to populate database"
        exit 1
    fi
    
    echo "✓ Database setup complete"
else
    echo "⚠️  Database setup skipped. Make sure to run schema.sql and populate.sql manually."
fi

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  python3 app.py"
echo ""
echo "Access the application at:"
echo "  http://127.0.0.1:5000"
echo ""
echo "Login credentials:"
echo "  Marine Officer: MARINE_HQ / SEAGULL"
echo "  CP0 Admin:      ROB_LUCCI / DARK_JUSTICE"
echo ""
echo "⚓ Justice Will Prevail ⚓"
