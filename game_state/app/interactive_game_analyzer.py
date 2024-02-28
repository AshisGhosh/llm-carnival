import asyncio
import uuid

from shared.utils.client_utils import check_model_server_status, generate_text_gemma_2b_it, process_image_blip, generate_text_openrouter

from langfuse import Langfuse
langfuse = Langfuse()

class InteractiveGameAnalyzer:
    def __init__(self):
        self.llm = generate_text_openrouter
        self.llm_name = "gemini-7b-it"
        self.vqa = process_image_blip
        self.vqa_name = "blip"
        self.models_initialized = False
        self.model_status = "Models not initialized. Please wait."
        self.context = []
        self.max_questions = 10
        self.questions_asked = 0
        self.global_session_id = uuid.uuid4().hex
        self.trace_id = None
        self.span_id = None
        self.error_message = None
    
    async def ask_question(self, image):
        # Generate a question based on the current context
        prompt = self.generate_question_prompt(self.context)
        
        question = await self.generate_question(prompt)
        if not question:
            return False
        if "LEARNED_ENOUGH" in question:
            return "LEARNED_ENOUGH"
        
        question = await self.validate_question(question)
        if not question:
            return False
        
        return await self.get_vqa_response(question, image)

    async def get_vqa_response(self, question, image):
        input = {
            "question": question,
            "image": self.image_name
        }
        generation = langfuse.generation(
            trace_id = self.trace_id,
            parent_observation_id = self.span_id,
            name="get-vqa-response",
            model=self.vqa_name,
            model_parameters={},
            input=input,
            metadata=None
        )
        # Get the response from the VQA model
        res = await self.vqa(question, image)
        generation.end(
            output=res
        )
        if not res["success"]:
            self.error_message = res["text"]
            print(f"Error getting VQA response: {res['text']}")
            return False
        answer = res["answer"]
        self.update_context(question, answer)
        return answer

    def generate_question_prompt(self, context):
        nl = "\n"
        if self.questions_asked == 0:
            intro = "Ask me a question about a video game that would help determine the next action."
            combat_scenario = "Focus on if we are in a combat scenario and if so, what is the state of the combat."
            prompt = f"{intro} {combat_scenario} {nl} What is your first question?"
        else:
            answer = context[-1][1]
            answer = f"The answer to your last question was: {answer}"
            questions_remaining = self.max_questions - self.questions_asked
            question_limit_info = f"You can ask {questions_remaining} more questions."
            question_advice = "Try asking a multiple choice question or a yes/no question."
            question_instruction = "Only respond with the question."
            prompt_for_question = "What is your next question?"
            prompt = f"{answer} {nl} {question_limit_info} {question_advice} {question_instruction} {nl} {prompt_for_question}"

        print(f"Generated prompt: {prompt}")
        return prompt
    
    async def generate_question(self, prompt):
        input = {
            "prompt": prompt,
            "session_id": self.trace_id
        }
        generation = langfuse.generation(
            trace_id = self.trace_id,
            parent_observation_id = self.span_id,
            name="generate-question",
            model=self.llm_name,
            model_parameters={},
            input=input,
            metadata=None
        )
        res = await self.llm(prompt=prompt, session_id=self.trace_id)
        generation.end(
            output=res
        )
        if not res["success"]:
            self.error_message = res["text"]
            print(f"Error generating question: {res['text']}")
            return False
        question = res["text"]
        print(f"Generated question: {question}")
        return question

    async def validate_question(self, question):
        validation_instruction = "You are professional and efficient with your responses. In this text, extract just the single question that is meant to be asked and any possible answer responses included:"
        prompt = f"{validation_instruction} {question}"
        input = {
            "prompt": prompt,
            "session_id": self.trace_id
        }
        generation = langfuse.generation(
            trace_id = self.trace_id,
            parent_observation_id = self.span_id,
            name="validate-question",
            model=self.llm_name,
            model_parameters={},
            input=input,
            metadata=None
        )
        res = await self.llm(prompt=prompt, session_id=None)
        generation.end(
            output=res
        )
        if not res["success"]:
            self.error_message = res["text"]
            print(f"Error validating question: {res['text']}")
            return False
        question = res["text"]
        print(f"Validated question: {question}")
        return question

    def update_context(self, question, answer):
        # Update the context with the latest Q&A
        print(f"Adding Q: {question} A: {answer} to context")
        self.context.append((question, answer))
    
    async def generate_summary(self, context, session_id=None):
        # Generate a summary of the context
        nl = "\n"
        summary_prompt = "Read the following converation and return just the salient points about the game."
        context_descriptor = "Here is a conversation about it in a format of `Questions` and `Answers`:"
        context = f"{nl}".join([f"Question: {q} Answer: {a}" for q, a in context])
        prompt = f"{summary_prompt} {context_descriptor} {context}"

        generation = langfuse.generation(
            trace_id = self.trace_id,
            name="generate-summary",
            model=self.llm_name,
            model_parameters={},
            input=prompt,
            metadata=None
        )
        res = await self.llm(prompt=prompt, session_id=session_id)
        generation.end(
            output=res
        )
        if not res["success"]:
            self.error_message = res["text"]
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
        self.trace_id = uuid.uuid4().hex
        self.image_name = "screenshot"
        metadata=None
        input = {
            "image": self.image_name,
            "session_id": self.trace_id
        }
        trace = langfuse.trace(
            name="analyze-screenshot",
            id = self.trace_id,
            user_id="ashis",
            session_id=self.global_session_id,
            input=input,
            metadata=metadata,
            tags=["generate-text", "gemma-2b-it"]
        )
        
        self.questions_asked = 0  # Reset the counter for each new screenshot
        self.context = []  # Reset the context for each new screenshot
        while self.questions_asked < self.max_questions:
            span = trace.span(
                name="ask-question",
                input=input
                )
            self.span_id = span.id
            response = await self.ask_question(image)
            if not response:
                error_message = f"Error asking question: {self.error_message}"
                print(error_message)
                span.end(
                    output=error_message
                )
                trace.update(
                    output=error_message
                )
                return success, error_message
            span.end(
                output=self.context
            )
            self.span_id = None
            self.questions_asked += 1

            if self.is_done(response):
                break

        success = True
        analysis = {}
        analysis["summary"] = await self.generate_summary(self.context)
        if not analysis["summary"]:
            error_message = f"Error generating summary: {self.error_message}"
            success = False

        analysis ["context"] = self.context
        trace.update(
            output=analysis
        )
       
        return success, analysis

    def is_done(self, response):
        # Determine whether enough information has been gathered
        # ...
        if 'LEARNED_ENOUGH' in response:
            print("Learned enough.")
        return 'LEARNED_ENOUGH' in response

