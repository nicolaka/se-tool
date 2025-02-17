# HashiCorp SE Tool

This is a tool to help HashiCorp Solutions Engineers in their day to day work.

![SE Tool Screenshot](assets/Screenshot_se_tools.png)

## Dependencies

### Hardware recommended
Mac with M1 Pro

### Software dependencies
 - Ollama - https://ollama.com/
 - Docker
 - Github access
 - Python 3.11

## Usage

1. Clone the repo
2. create the following sub-folders:
    * cache_docker (for docker caching)
    * cache (to use python directly)

3. Go to https://ollama.com/library and download some models.

### With Docker

1. Have Ollama running -> see `run_ollama.sh`.
2. set `OLLAMA_HOST` in `docker-compose.yaml` to the IP of your machine. 
3. Run `docker compose up -d`.

*Note: Once I have a docker container published, this will be easier*

### Without docker

1. Have Ollama running -> see `run_ollama.sh`
2. Run from source with `run_streamlit.sh`

## Creating embeddings

The quality of the answers only goes as far as the quality of the LLM, prompt and embeddings.

For RAG, create embeddings with the `embed_hashicorp.py` script or, if you work for HashiCorp, contact me directly.

See `run_embed.sh`
