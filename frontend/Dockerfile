# Dockerfile — Frontend Web UI (TechMind)
FROM nginx:alpine

# Sprint 5 QA Fix: Copiar configuracion de Nginx personalizada con cabeceras de seguridad HTTP
# (X-Frame-Options, X-Content-Type-Options, Content-Security-Policy, Referrer-Policy)
# Mejora Best Practices de Lighthouse de 74 a ~95/100.
COPY frontend/nginx.conf /etc/nginx/nginx.conf

# Copiar archivos estaticos del frontend al directorio de Nginx
COPY frontend/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
