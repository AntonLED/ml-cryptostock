FROM node:18-alpine 

WORKDIR /react-app

COPY ./package*.json /react-app/

RUN npm install recharts

RUN npm install

COPY . .

EXPOSE 3000

CMD [ "npm" , "start" ]