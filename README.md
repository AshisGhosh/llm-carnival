# LLM Carnival
Building a decision making agent via scene understanding with iteratively composed LLMs, and tree of thoughts strategy generation and evaluation. 

In this iteration, the use case is geared towards video games but the project has been inspired my robot planning and execution in physical, real-world scenarios.


## Overview

This project takes a microservices approach where each microservice is isolated in it's own docker container while providing FastAPI endpoints. 

* **Model Server** - hosts local Hugginface models and also connects to model APIs. Primarily making use of Openrouter.ai, emphasis on interoperatbility between different models.
* **Game State** - Uses a more capable LLM (Gemini 7B-it) to iteratively understand the scene with a quick and efficient VQA model (BLIP)
* **Action Decision** - The decision making engine powered via an LLM (Gemini 7B-it) to build Tree of Thoughts reasoning to determine the next step with self critique.
* **Frontend** - A simple front end built with NextJS/React to show status of interpreting game state and making a decision


### Technology Stack & Diagram

Special shoutout to [Langfuse](https://langfuse.com/) and [Openrouter.ai](https://openrouter.ai/) for working with me to update their products so this project could happen.
