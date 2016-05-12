#!/bin/bash

###
# This script builds the project and exports the Lider Console product for Linux (x32, x64), Windows (x32, x64) and MacOSX.
#
# Exported products can be found under /tmp/lider-console
###

PRJ_ROOT_PATH=$(readlink -f ..)
echo "Project path: $PRJ_ROOT_PATH"

# Generate third-party dependencies
echo "Generating third-party dependencies..."
cd "$PRJ_ROOT_PATH"/lider-console-remote-access-dependencies
mvn clean p2:site
echo "Generated third-party dependencies."

# Start jetty server for Tycho to use generated dependencies
echo "Starting server for Tycho..."
mvn jetty:run &
J_PID=$!
echo "Started server."

# Build project
echo "Building plugin project..."
cd "$PRJ_ROOT_PATH"
mvn clean install -DskipTests
echo "Plugin project built successfully."

# After exporting products, kill jetty server process
echo "Shutting down server..."
kill $J_PID
echo "Server shut down."

EXPORT_PATH=/tmp/remote-access
echo "Export path: $EXPORT_PATH"

# Copy resulting files
echo "Copying resulting files to $EXPORT_PATH..."
mkdir -p "$EXPORT_PATH"
cp -rf "$PRJ_ROOT_PATH"/lider-remote-access/target/*.jar "$EXPORT_PATH"
cp -rf "$PRJ_ROOT_PATH"/lider-console-remote-access/target/*.jar "$EXPORT_PATH"
echo "Copied resulting files."

echo "Built finished successfully!"
echo "Files can be found under: $EXPORT_PATH"
