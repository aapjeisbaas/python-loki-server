FROM python:bullseye AS builder
USER root
WORKDIR /build
COPY . /build
RUN apt update && apt install -y upx-ucl
RUN pip3 install -r requirements.txt
RUN pyinstaller -s -F http-server.py
RUN mkdir -p -m 1777 /output/tmp
RUN staticx /build/dist/http-server /output/http-server.sx ; chmod 755 /output/http-server.sx


FROM scratch
WORKDIR /
USER root
COPY --from=builder /output /
CMD ["/http-server.sx"]
EXPOSE 8080/tcp
USER 1001