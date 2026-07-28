# Dockerfile — Backend Spring Boot Java 17 (TechMind)
FROM eclipse-temurin:17-jdk-alpine AS build
WORKDIR /app

# Copiar configuración Maven y código fuente
COPY backend/api/api/mvnw .
COPY backend/api/api/.mvn .mvn
COPY backend/api/api/pom.xml .
COPY backend/api/api/src src

# Dar permisos de ejecución al wrapper de Maven y compilar jar
RUN chmod +x mvnw && ./mvnw package -DskipTests

# Etapa 2 — Imagen liviana de ejecución
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
