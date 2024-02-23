import threading
import asyncio

from shared.models.huggingface_vqa import HuggingFaceBLIPforVQA
from shared.models.huggingface_llm import HuggingFaceGPT2LLM


class InteractiveGameAnalyzer:
    def __init__(self):
        self.llm = None
        self.vqa = None
        self.models_initialized = False
        self.model_status = "Models not initialized. Please wait."
        self.context = []
        self.max_questions = 1
        self.questions_asked = 0
        threading.Thread(target=self.initialize_models, daemon=True).start()        
    
    def initialize_models(self):
        # Initialize the VQA and LLM models
        self.model_status = "Initializing models..."
        print(self.model_status)
        self.llm = HuggingFaceGPT2LLM()
        self.model_status = "LLM initialized. Initializing VQA..."
        print(self.model_status)
        self.vqa = HuggingFaceBLIPforVQA()
        if self.llm and self.vqa:
            self.model_status = "LLM and VQA initialized."
            self.models_initialized = True
        else:
            self.model_status = "Error initializing models."
        print(self.model_status)

    def ask_question(self, image):
        # Generate a question based on the current context
        prompt = self.generate_question_prompt(self.context)
        question = self.llm.generate(prompt)
        print(f"Generated question: {question}")
        return self.get_vqa_response(image, question)

    def get_vqa_response(self, image, question):
        # Get the response from the VQA model
        # answer = self.vqa.process_image(image, question)
        answer = "cheese"
        self.update_context(question, answer)
        return answer

    def generate_question_prompt(self, context):
        intro = "You are trying to understand a screenshot of a video game by interacting with a VQA model that can offer one-word responses."

        context_summary = " ".join([f"Q: {q} A: {a}" for q, a in context])

        questions_remaining = self.max_questions - self.questions_asked
        question_limit_info = f"You can ask {questions_remaining} more questions."

        prompt = f"{intro} {context_summary} {question_limit_info} What should be the next question? Or tell me if you've learned enough."
        return prompt

    def update_context(self, question, answer):
        # Update the context with the latest Q&A
        print(f"Adding Q: {question} A: {answer} to context")
        self.context.append((question, answer))
    
    def generate_summary(self, context):
        # Generate a summary of the context
        return " ".join([f"Q: {q} A: {a}" for q, a in context])

    async def analyze_screenshot(self, image):
        success = False
        if not self.models_initialized:
            return success, self.model_status
        
        print("Analyzing screenshot...")
        self.questions_asked = 0  # Reset the counter for each new screenshot
        self.context = []  # Reset the context for each new screenshot
        while self.questions_asked < self.max_questions:
            response = self.ask_question(image)
            self.questions_asked += 1

            if self.is_done(response):
                break
        
        analysis = {}
        analysis["summary"] = self.generate_summary(self.context)
        analysis ["context"] = self.context
        success = True
        return success, analysis

    def is_done(self, response):
        # Determine whether enough information has been gathered
        # ...
        if 'learned enough' in response.lower():
            print("Learned enough.")
        return 'learned enough' in response.lower()

