# ─────────────────────────────────────────────────────
#  Maintenance Wizard — Frontend (React + Vite)
#  Railway deployment — Nginx serves the built SPA
# ─────────────────────────────────────────────────────

# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --silent

COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx config: handle React Router (SPA) routes
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
