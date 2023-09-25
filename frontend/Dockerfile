# Use the official Node.js 14 image as the base image
FROM node:18

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package.json ./

# Install the dependencies
RUN npm ci

# Copy the rest of the application code to the container
COPY . .

# Build the Next.js app
RUN npm run build

# Expose the port on which the app will run
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "start"]
