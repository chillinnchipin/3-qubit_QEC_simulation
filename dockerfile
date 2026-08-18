# Setup project
FROM python:3.12-bookworm
WORKDIR /quant_comp_project/

# Set enviornment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install depencies
COPY requirements.txt /quant_comp_project/
RUN pip install -r requirements.txt --no-cache-dir

# Copy source files
COPY src/ /quant_comp_project/src/
COPY tests/ /quant_comp_project/tests/
COPY .git /quant_comp_project/

# Run test
#RUN pytest

# Run on entrance
CMD ["python", "src/qec.py"]
