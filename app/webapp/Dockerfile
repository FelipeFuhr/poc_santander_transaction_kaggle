# First Stage

FROM golang:1.13 as builder

ENV GO111MODULE=auto

WORKDIR $GOPATH/src/app

COPY . .

RUN go mod download

WORKDIR $GOPATH/src/app/loadTemplate
RUN go mod download

WORKDIR $GOPATH/src/app

RUN go build -o $GOPATH/bin .

# Second Stage

FROM ubuntu:20.04

COPY --from=builder /go/bin/app /app
COPY ./loadTemplate/template /template

EXPOSE 9000

ENTRYPOINT ["./app"]