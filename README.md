# MEWT Backend - Marker Engine with Emotion Analysis

Backend for the MEWT (Marker Engine with Emotion Analysis) system.

## Quick Start

```bash
# Install dependencies
npm install

# Start the server
npm start
```

The server will run on `http://localhost:8000`

## API Endpoints

- `POST /emotion` - Analyze emotion in text
- `GET /status` - Health check endpoint
- `GET /openapi.yaml` - API documentation

## Deployment

### Fly.io Deployment

This application is configured for deployment on Fly.io:

```bash
# Deploy to Fly.io
fly deploy
```

### Docker Deployment

```bash
# Build the image
docker build -t mewt-backend .

# Run the container
docker run -p 8000:8000 mewt-backend
```

## License

Creative Commons BY-NC-SA 4.0
