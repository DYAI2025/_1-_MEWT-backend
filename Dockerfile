# Use the official Node.js 18 runtime as base image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["npm", "start"]