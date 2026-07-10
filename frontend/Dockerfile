FROM node:20-alpine

LABEL maintainer="Aditya Bawne"

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=5 \
CMD wget --spider -q http://127.0.0.1:3000 || exit 1

CMD ["npm", "start"]