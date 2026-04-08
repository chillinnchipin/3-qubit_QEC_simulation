# Setup project
FROM python:3.12-bookworm
WORKDIR /quant_comp_project/

# Install depencies
COPY requirements.txt /quant_comp_project/
RUN pip install -r requirements.txt --no-cache-dir

# Copy source files
COPY main.py /quant_comp_project/
COPY functions.py /quant_comp_project/
COPY test_functions.py /quant_comp_project/
COPY .git /quant_comp_project/

# Run test

# Run on entrance
CMD ["python3", "main.py"]
