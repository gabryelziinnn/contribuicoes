FROM public.ecr.aws/lambda/python:3.9
LABEL author="Gabryel Bento"
WORKDIR /usr/src/app

COPY * ./ 
RUN python3.9 -m pip install -r requirements.txt -t 

CMD ["lambda_function.lambda_handler"]