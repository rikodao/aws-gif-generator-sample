FROM public.ecr.aws/lambda/python:3.11

# COPY requirements.txt ./

# RUN python3.11 -m pip install -r requirements.txt -t .
RUN pip install --no-cache-dir numpy==1.24.2 moviepy pillow==9.5.0

COPY app.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
