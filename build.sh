docker build -t pyppeteer-image .
docker run -d -p 5006:5006 --name pyppeteer pyppeteer-image:latest
docker update pyppeteer --restart=always