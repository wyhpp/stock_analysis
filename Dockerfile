FROM python:3.11

LABEL name="stock_analysis"
LABEL version="0.1.0"
LABEL description="Chinese stock statistics analysis"

WORKDIR /app

ADD . ./

# CMD ["python"]