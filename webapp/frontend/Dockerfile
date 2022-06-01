FROM docker.io/node:18 as build

WORKDIR /app
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json

RUN npm ci
COPY . /app

RUN node_modules/.bin/ng build

FROM docker.io/nginx:1.21.6

COPY --from=build /app/dist /usr/share/nginx/html