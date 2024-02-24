import threading
import asyncio

from shared.utils.client_utils import check_model_server_status, generate_text_gemma_2b_it, process_image_blip

class InteractiveGameAnalyzer:
    def __init__(self):
        self.llm = generate_text_gemma_2b_it
        self.vqa = process_image_blip
        self.models_initialized = False
        self.model_status = "Models not initialized. Please wait."
        self.context = []
        self.max_questions = 5
        self.questions_asked = 0
    
    async def ask_question(self, image):
        # Generate a question based on the current context
        prompt = self.generate_question_prompt(self.context)
        res = await self.llm(prompt=prompt)
        if not res["success"]:
            print(f"Error generating question: {res['text']}")
            return False
        question = res["text"]
        print(f"Generated question: {question}")

        return await self.get_vqa_response(question, image)

    async def get_vqa_response(self, question, image):
        # Get the response from the VQA model
        res = await self.vqa(question, image)
        if not res["success"]:
            print(f"Error getting VQA response: {res['text']}")
            return False
        answer = res["answer"]
        self.update_context(question, answer)
        return answer

    def generate_question_prompt(self, context):
        intro = "You are trying to understand a screenshot of a video game by interacting with a VQA model that can offer one-word responses."

        context_summary = " ".join([f"Q: {q} A: {a}" for q, a in context])
        if context_summary:
            context_summary = f"Here is some context: {context_summary}"

        questions_remaining = self.max_questions - self.questions_asked
        question_limit_info = f"You can ask {questions_remaining} more questions."

        prompt = f"{intro} {context_summary} {question_limit_info} What should be the next question? Or tell me if you've learned enough."
        print(f"Generated prompt: {prompt}")
        return prompt

    def update_context(self, question, answer):
        # Update the context with the latest Q&A
        print(f"Adding Q: {question} A: {answer} to context")
        self.context.append((question, answer))
    
    async def generate_summary(self, context):
        # Generate a summary of the context
        summary_prompt = "You are trying to understand the state of a video game. Here is a conversation about it: "
        context = " ".join([f"Q: {q} A: {a}" for q, a in context])
        ask_prompt = "Summarize the understanding of the state of the game given the conversation."
        prompt = f"{summary_prompt} {context} {ask_prompt}"
        res = await self.llm(prompt=prompt)
        if not res["success"]:
            print(f"Error generating summary: {res['text']}")
            return False
        return res["text"]

    async def analyze_screenshot(self, image):
        success = False
        if not self.models_initialized:
            if not await check_model_server_status():
                print(self.model_status)
                return success, self.model_status
            self.models_initialized = True
        
        print("Analyzing screenshot...")
        self.questions_asked = 0  # Reset the counter for each new screenshot
        self.context = []  # Reset the context for each new screenshot
        while self.questions_asked < self.max_questions:
            response = await self.ask_question(image)
            if not response:
                print("Error asking question.")
                return success, "Error asking question."
            self.questions_asked += 1

            if self.is_done(response):
                break

        
        analysis = {}
        analysis["summary"] = await self.generate_summary(self.context)
        analysis ["context"] = self.context
        success = True
        return success, analysis

    def is_done(self, response):
        # Determine whether enough information has been gathered
        # ...
        if 'learned enough' in response.lower():
            print("Learned enough.")
        return 'learned enough' in response.lower()

